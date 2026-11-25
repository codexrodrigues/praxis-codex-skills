"""Conservative static source evidence. This module does not approve runtime behavior."""
import re


def masked_java(source):
    return re.sub(r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*.*?\*/',
                  lambda m: " " * len(m.group()), source, flags=re.DOTALL)


def end_delimiter(text, start, opening, closing):
    depth = 0
    for index in range(start, len(text)):
        if text[index] == opening:
            depth += 1
        elif text[index] == closing:
            depth -= 1
            if depth == 0:
                return index
    return -1


def java_methods(source):
    mask = masked_java(source)
    result, boundary = {}, 0
    for match in re.finditer(r'\b(?:public|protected|private)\s+(?:[\w<>,.?\[\]]+\s+)+(\w+)\s*\(', mask):
        start = mask.find("(", match.start())
        end = end_delimiter(mask, start, "(", ")")
        brace, semicolon = mask.find("{", end), mask.find(";", end)
        if end < 0 or brace < 0 or (semicolon >= 0 and semicolon < brace):
            continue
        close = end_delimiter(mask, brace, "{", "}")
        if close >= 0:
            result[match.group(1)] = (source[boundary:match.start()], source[match.start():brace], source[brace+1:close])
            boundary = close + 1
    return result


def technical_or_mirrored(name, annotations, technical_names):
    if re.search(r'@(?:\w+\.)*(?:Id|EmbeddedId|Version|OneToMany|ManyToMany|Formula)\b', annotations):
        return True
    if name in technical_names and "@Embedded" in annotations:
        return True
    joins=re.findall(r'@(?:\w+\.)*JoinColumn\s*\(([^)]*)\)',annotations,re.DOTALL)
    return bool(re.search(r'@(?:\w+\.)*(?:ManyToOne|OneToOne)\b', annotations) and joins
                and all(re.search(r'insertable\s*=\s*false',join) and re.search(r'updatable\s*=\s*false',join)
                        and not re.search(r'(?:insertable|updatable)\s*=\s*true',join) for join in joins))


def mapped_input_fields(entity, dto_fields, classes):
    found = set()
    for info in classes.values():
        if not re.search(r'\bResourceMapper\s*<\s*' + re.escape(entity) + r'\s*,', info.content):
            continue
        code=masked_java(info.content)
        mappings=[]
        for annotation in re.finditer(r'@(?:\w+\.)*Mapping\s*\(',code):
            start=code.find("(",annotation.start())
            end=end_delimiter(code,start,"(",")")
            if end>=0:mappings.append(info.content[start+1:end])
        for field in dto_fields:
            accessor = re.escape(field[:1].upper() + field[1:])
            direct = re.search(r'\bentity\.set' + accessor + r'\s*\(\s*dto\.get' + accessor + r'\s*\(\s*\)\s*\)', code)
            explicit = any(re.search(r'target\s*=\s*"' + re.escape(field) + '"', item)
                           and re.search(r'source\s*=\s*"' + re.escape(field) + '"', item)
                           and not re.search(r'ignore\s*=\s*true', item) for item in mappings)
            if direct or explicit:
                found.add(field)
    return found


def command_fields(ctrl, entity, classes):
    methods = {name: java_methods(info.content) for name, info in classes.items()}
    implementors = {}
    for cls_name, cls_info in classes.items():
        impl_match = re.search(
            r'\b(?:class|record)\s+\w+[^{]*?\bimplements\s+([^{]+)',
            masked_java(cls_info.content),
            re.DOTALL,
        )
        if impl_match:
            clean_impls = re.sub(r'<[^>]*>', '', impl_match.group(1))
            for iface in re.findall(r'\b([A-Za-z_]\w*)', clean_impls):
                implementors.setdefault(iface, []).append(cls_name)
    roots = [name for name, (header, _, _) in methods[ctrl.name].items()
             if re.search(r'@(?:\w+\.)*(?:WorkflowAction|ResourceIntent)\b', masked_java(header))
             and re.search(r'@(?:\w+\.)*(?:PostMapping|PatchMapping)\b', masked_java(header))]
    result, visited = set(), set()

    def visit(owner, method):
        if (owner, method) in visited or method not in methods.get(owner, {}):
            return
        visited.add((owner, method))
        info = classes[owner]
        if re.search(r'\bResourceMapper\s*<', info.content):
            return
        _, signature, body = methods[owner][method]
        code=masked_java(body)
        variables = set(re.findall(r'\b' + re.escape(entity) + r'\s+(\w+)\b', masked_java(signature) + "\n" + code))
        variables.update(re.findall(r'\bvar\s+(\w+)\s*=\s*new\s+' + re.escape(entity) + r'\b', code))
        for receiver, setter in re.findall(r'\b(\w+)\.set([A-Z]\w*)\s*\(', code):
            if receiver in variables:
                result.add(setter[:1].lower() + setter[1:])
        fields = {name: type_.split("<")[0].split(".")[-1] for type_, name, _ in info.fields}
        for receiver, called in re.findall(r'\b(\w+)\.(\w+)\s*\(', code):
            target = fields.get(receiver, receiver if receiver in classes else owner if receiver == "this" else "")
            if target in classes and methods.get(target):
                visit(target, called)
            elif target in implementors:
                for impl_name in implementors[target]:
                    visit(impl_name, called)
        for called in re.findall(r'(?<![.\w])([a-zA-Z_]\w*)\s*\(', masked_java(body)):
            visit(owner, called)
    for root in roots:
        visit(ctrl.name, root)
    return result


def relationship_key_fields(entity_fields):
    """Match scalar JPA columns to single-column declared joins; skip composite @JoinColumns."""
    joins = set()
    for _, _, annotations in entity_fields:
        if re.search(r'@(?:\w+\.)*(?:ManyToOne|OneToOne)\b', annotations):
            cols = re.findall(r'@(?:\w+\.)*JoinColumn\s*\([^)]*?\bname\s*=\s*"([^"]+)"', annotations)
            if len(cols) == 1:
                joins.add(cols[0])
    return {field for _, field, annotations in entity_fields
            if any(column in joins for column in re.findall(r'@(?:\w+\.)*Column\s*\([^)]*?\bname\s*=\s*"([^"]+)"', annotations))}


def presentation_issues(type_, field, annotations, foreign_keys=()):
    mask = masked_java(annotations)
    m = re.search(r'@(?:[\w.]+\.)?UISchema\s*\(', mask)
    if not m:
        return [f"{field}: missing @UISchema"]
    start = mask.find("(", m.start())
    end = end_delimiter(mask, start, "(", ")")
    body = annotations[start + 1 : end] if end >= 0 else ""
    reference = "@ResourceReference" in annotations or bool(re.search(r'@(?:[\w.]+\.)?ResourceReference\b', annotations))
    semantic = type_ in {"LocalDate", "LocalDateTime", "BigDecimal", "java.math.BigDecimal"} or field in foreign_keys or reference and "ENTITY_LOOKUP" in body
    issues = []
    if semantic:
        for attr in ("type", "controlType", "icon"):
            if not re.search(r'\b' + attr + r'\s*=\s*(?:"[^" ]+"|[\w.]+)', body):
                issues.append(f"{field}: explicit {attr} required for date/amount/relationship")
    if field in foreign_keys and "ENTITY_LOOKUP" not in body:
        issues.append(f"{field}: declared relationship requires ENTITY_LOOKUP")
    if "ENTITY_LOOKUP" in body and not re.search(r'endpoint\s*=\s*"[^"]*/option-sources/[^/]+/options/filter"', body):
        issues.append(f"{field}: lookup requires a named RESOURCE_ENTITY option source")
    if type_ in {"LocalDate", "LocalDateTime"} and not re.search(r'FieldControlType\.(?:DATE_PICKER|DATE_TIME_PICKER)\b', body):
        issues.append(f"{field}: scalar date requires a date control")
    if type_ == "List<LocalDate>" and "DATE_RANGE" not in body:
        issues.append(f"{field}: date interval requires DATE_RANGE")
    return issues


def resource_fact_editorial_issues(source, owner_name):
    issues = []
    for fact in re.findall(r'@(?:\w+\.)*ResourceFact\s*\((.*?)\)', source, re.DOTALL):
        key_m = re.search(r'key\s*=\s*"([^"]+)"', fact)
        lbl_m = re.search(r'label\s*=\s*"([^"]+)"', fact)
        if lbl_m:
            lbl = lbl_m.group(1).strip()
            if len(lbl) > 36 or lbl.endswith("."):
                key_name = key_m.group(1) if key_m else "unknown"
                issues.append(f"{owner_name}@ResourceFact({key_name}): label looks like a sentence/description ('{lbl}')")
    return issues


def dto_table_visibility_issues(dto_name, fields):
    ui_fields = [(name, ann) for _, name, ann in fields if "@UISchema" in ann]
    if len(ui_fields) < 15:
        return []
    hidden = [
        name for name, ann in ui_fields
        if re.search(r'tableHidden\s*=\s*true', ann)
    ]
    if len(hidden) == 0:
        return [
            f"{dto_name}: {len(ui_fields)} @UISchema fields have 0 tableHidden=true (>= 15 fields); mark secondary detail fields with tableHidden=true"
        ]
    return []


def entity_lookup_descriptor_issues(classes):
    issues = []
    for info in classes.values():
        cleaned = masked_java(info.content)
        for match in re.finditer(r'new\s+(?:[\w.]+\.)?EntityLookupDescriptor\s*\(', cleaned):
            start = cleaned.find("(", match.start())
            end = end_delimiter(cleaned, start, "(", ")")
            if end < 0:
                continue
            args = []
            boundary, depth = start + 1, 0
            for index in range(start + 1, end):
                char = cleaned[index]
                if char in '({[': depth += 1
                elif char in ')}]': depth -= 1
                elif char == ',' and depth == 0:
                    args.append(cleaned[boundary:index].strip())
                    boundary = index + 1
            args.append(cleaned[boundary:end].strip())
            # Optional paths/URLs in nested contracts are legitimate. Count only outer arguments,
            # and require the four actual rich subcontracts (canonical 13- or 15-argument constructor).
            null_count = sum(arg == 'null' for arg in args)
            missing = len(args) not in (13, 15) or any(args[i] == 'null' for i in (8, 10, 11, 12))
            if missing:
                issues.append(
                    f"{info.name}: skeletal EntityLookupDescriptor ({null_count} null arguments; populate LookupSelectionPolicy, LookupDetailDescriptor, LookupDisplayDescriptor, LookupFilteringDescriptor)"
                )
                break
    return issues


def micro_visualization_properties(dto_name, classes, fields):
    """Count annotated public bean properties, including inherited zero-argument getters."""
    result = {name for _, name, ann in fields
              if re.search(r'@(?:[\w.]+\.)?MicroVisualization\b', masked_java(ann))}
    visited = set()
    while dto_name in classes and dto_name not in visited:
        visited.add(dto_name)
        info = classes[dto_name]
        for name, (header, signature, _) in java_methods(info.content).items():
            if (re.fullmatch(r'get[A-Z]\w*', name)
                    and re.search(r'\bpublic\b', signature)
                    and re.search(r'\(\s*\)', signature)
                    and re.search(r'@(?:[\w.]+\.)?MicroVisualization\b', masked_java(header))):
                result.add(name[3:4].lower() + name[4:])
        parent = re.search(r'\bclass\s+\w+\s+extends\s+(\w+)', masked_java(info.content))
        dto_name = parent.group(1) if parent else ''
    return result


def reactive_determination_count(controller_source, classes):
    """Count ReactiveDeterminationDefinition bindings matching real POST/PUT/PATCH operationIds on the controller."""
    det_endpoint_ops = set()
    form_ops = set()
    for _, (header, _, _) in java_methods(controller_source).items():
        uncommented_hdr = re.sub(r'//[^\n]*|/\*.*?\*/', '', header, flags=re.S)
        op_match = re.search(r'operationId\s*=\s*"([^"]+)"', uncommented_hdr)
        if not op_match:
            continue
        op_id = op_match.group(1)
        if re.search(r'@(?:[\w.]+\.)?(?:WorkflowAction|BulkOperation)\b', uncommented_hdr):
            continue
        if re.search(r'@(?:[\w.]+\.)?PostMapping\s*\(\s*[^)\s]', uncommented_hdr):
            det_endpoint_ops.add(op_id)
        elif re.search(r'@(?:[\w.]+\.)?(?:PostMapping|PutMapping|PatchMapping)\b', uncommented_hdr):
            form_ops.add(op_id)
    if not det_endpoint_ops and not form_ops:
        return 0
    provider_literals = set()
    for info in classes.values():
        cleaned = re.sub(r'//[^\n]*|/\*.*?\*/', '', info.content, flags=re.S)
        if not re.search(r'\bnew\s+(?:[\w.]+\.)?ReactiveDeterminationDefinition\s*\(', cleaned):
            continue
        provider_literals.update(re.findall(r'"([^"]+)"', cleaned))
    matched_det = det_endpoint_ops & provider_literals
    if matched_det:
        return len(matched_det)
    return 1 if (form_ops & provider_literals) else 0


def reactive_determination_issues(classes):
    """Detect invalid JSON Pointers in ReactiveDeterminationInputBinding / ReactiveDeterminationOutputBinding."""
    issues = []
    for info in classes.values():
        cleaned = re.sub(r'//[^\n]*|/\*.*?\*/', '', info.content, flags=re.S)
        for match in re.finditer(
            r'\bnew\s+(?:[\w.]+\.)?ReactiveDetermination(?:Input|Output)Binding\s*\(\s*"([^"]*)"\s*,\s*"([^"]*)"\s*\)',
            cleaned,
        ):
            for ptr in (match.group(1), match.group(2)):
                if not ptr.startswith("/"):
                    issues.append(
                        f"{info.name}: invalid JSON Pointer '{ptr}' in ReactiveDetermination binding (must start with '/')"
                    )
    return issues


def relationship_display_fields(entity, fields, classes):
    relations = {name for _, name, ann in fields if re.search(r'@(?:ManyToOne|OneToOne)\b', ann)}
    result = set()
    for info in classes.values():
        if not re.search(r'\bResourceMapper\s*<\s*' + re.escape(entity) + r'\s*,', info.content):
            continue
        code = masked_java(info.content)
        for relation in relations:
            accessor = relation[:1].upper() + relation[1:]
            pattern = r'dto\.set([A-Z]\w*)\s*\(\s*(?:entity\.get' + accessor + r'\(\)\s*==\s*null\s*\?\s*null\s*:\s*)?entity\.get' + accessor + r'\(\)\.get\w+\s*\('
            result.update(name[:1].lower() + name[1:] for name in re.findall(pattern, code))
    return result


RUNTIME_GATES = {"schema", "http", "availability", "persistence", "parity", "angularReadiness", "coldQueries", "reactiveDeterminations", "governedDecisions", "bulkOperations"}


def bulk_source_summary(controller_source, update_fields):
    """Reports structural opt-ins, never durable readiness or authorization."""
    editable = {name: ann for _, name, ann in update_fields
                if re.search(r'@(?:\w+\.)*BulkEditable\b', ann)}
    methods = java_methods(controller_source)
    operations = {name: header for name, (header, _, _) in methods.items()
                  if re.search(r'@(?:\w+\.)*BulkOperation\s*\(', masked_java(header))}
    issues = []
    declared = bool(re.search(r'@(?:\w+\.)*BulkResourceOperations\b', masked_java(controller_source)))
    if (editable or operations) and not declared:
        issues.append("Bulk opt-in requires @BulkResourceOperations on the resource")
    for name, ann in editable.items():
        if 'BulkMode.DOMAIN_COMMAND' in ann:
            issues.append(name + ': DOMAIN_COMMAND is not a field-editing mode')
        if re.search(r'allowClear\s*=\s*true', ann) and not re.search(r'nullable\s*=\s*true', ann):
            issues.append(name + ': CLEAR requires explicit schema nullability')
    if editable:
        for mode in ('UNIFORM_UPDATE', 'PER_ITEM_UPDATE'):
            if any('BulkMode.' + mode in ann or not re.search(r'\bmodes\s*=', ann) for ann in editable.values()) and not any('BulkMode.' + mode in header for header in operations.values()):
                issues.append(mode + ': editable fields lack a real confirmation handler')
    operation_ids = set(re.findall(r'operationId\s*=\s*"([^"]+)"', controller_source))
    for name, header in operations.items():
        match = re.search(r'evaluationOperationId\s*=\s*"([^"]+)"', header)
        if not match or match[1] not in operation_ids:
            issues.append(name + ': evaluation operation is unresolved')
        if 'BulkMode.DOMAIN_COMMAND' in header and not re.search(r'@(?:\w+\.)*WorkflowAction\s*\([^)]*ActionScope\.COLLECTION', header, re.S):
            issues.append(name + ': DOMAIN_COMMAND requires COLLECTION WorkflowAction')
    return len(editable), len(operations), issues


def source_fingerprint(project):
    import hashlib
    digest = hashlib.sha256()
    pom = project / "pom.xml"
    if pom.is_file():
        digest.update(b"pom.xml\0")
        digest.update(pom.read_text(encoding="utf-8-sig").encode())
        digest.update(b"\0")
    for folder in ("src", "scripts/workspace"):
        base = project / folder
        if not base.exists():
            continue
        for file in sorted(base.rglob("*")):
            if file.is_file() and file.suffix in {".java", ".yml", ".yaml", ".ts", ".mjs", ".json"}:
                digest.update(file.relative_to(project).as_posix().encode())
                digest.update(b"\0")
                digest.update(file.read_text(encoding="utf-8-sig").encode())
                digest.update(b"\0")
    return digest.hexdigest()


def runtime_evidence_issues(project, manifest_path):
    """Checks receipts/provenance, not the truth of self-authored architectural approval."""
    import json, hashlib
    errors = []
    if not manifest_path.is_file():
        return ["Runtime evidence manifest is missing"]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    except (ValueError, OSError):
        return ["Runtime evidence manifest is invalid"]
    if manifest.get("sourceSha256") != source_fingerprint(project):
        errors.append("Runtime evidence is stale for the current host sources")
    gates = manifest.get("gates", {})
    for name in sorted(RUNTIME_GATES):
        gate = gates.get(name, {})
        status = gate.get("status")
        if status == "not-applicable":
            if not gate.get("reason", "").strip():
                errors.append(name + ": not-applicable requires an explicit reason")
            continue
        if status != "pass":
            errors.append(name + ": " + str(status or "missing"))
            continue
        artifacts = gate.get("artifacts", [])
        if not artifacts:
            errors.append(name + ": pass requires hashed evidence artifacts")
        for artifact in artifacts:
            file = (project / artifact.get("path", "")).resolve()
            if not file.is_relative_to(project.resolve()) or not file.is_file():
                errors.append(name + ": artifact missing or outside project")
            elif hashlib.sha256(file.read_bytes()).hexdigest() != artifact.get("sha256"):
                errors.append(name + ": artifact hash mismatch")
    return errors
