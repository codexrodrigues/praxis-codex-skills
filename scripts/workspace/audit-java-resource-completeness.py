#!/usr/bin/env python3
"""
Praxis Platform — Java Resource Completeness, Quick View & Editorial Quality Auditor

Audits a Java/Spring Boot host project using praxis-metadata-starter to detect:
1. Entity-to-DTO truncation (percentage of @Entity business fields exposed in ResponseDTO/CreateDTO/UpdateDTO).
2. Quick View / 360° readiness (@ResourceIdentity subtitleField/metadataFields, @UISchema quickViewVisible/quickViewOrder,
   @ResourceReference with previewSurfaceId, and READ_PROJECTION / VIEW @UiSurface).
3. @UISchema & @ResourceFact editorial quality (detects descriptions pasted as labels, LocalDate fields without DATE_PICKER,
   skeletal EntityLookupDescriptor, and excessive unhidden table columns in DTOs).
4. FilterDTO density (count of @Filterable fields, variety of FilterOperation, and @QuickFilter presence).
5. Praxis semantic capabilities (@UiSurface, @WorkflowAction, @ResourceIntent, @ResourceFact, @MicroVisualization, @UiAnalytics,
   and Governed Bulking @BulkEditable / @BulkResourceOperations / @BulkOperation).

Usage:
    python scripts/workspace/audit-java-resource-completeness.py <path-to-java-host-project> [--strict]
"""

from __future__ import annotations

import argparse
import re
import sys
from java_resource_audit import (
    technical_or_mirrored,
    mapped_input_fields,
    command_fields,
    relationship_key_fields,
    presentation_issues,
    relationship_display_fields,
    runtime_evidence_issues,
    bulk_source_summary,
    resource_fact_editorial_issues,
    dto_table_visibility_issues,
    entity_lookup_descriptor_issues,
    micro_visualization_properties,
    reactive_determination_count,
    reactive_determination_issues,
    masked_java,
    end_delimiter,
)
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

AUDIT_EXCLUDED_ENTITY_FIELDS = {
    "id",
    "createdAt",
    "updatedAt",
    "createdBy",
    "updatedBy",
    "version",
    "rowVersion",
    "criadoEm",
    "atualizadoEm",
    "criadoPor",
    "atualizadoPor",
    "auditoria",
}


@dataclass
class JavaClassInfo:
    name: str
    path: Path
    content: str
    superclass: Optional[str] = None
    is_entity: bool = False
    is_controller: bool = False
    is_service: bool = False
    resource_key: Optional[str] = None
    resource_path: Optional[str] = None
    controller_type_args: List[str] = field(default_factory=list)
    service_type_args: List[str] = field(default_factory=list)
    fields: List[Tuple[str, str, str]] = field(default_factory=list)  # (type, name, annotations)
    getters: List[Tuple[str, str, str]] = field(default_factory=list)  # (type, prop, annotations)


def strip_comments(source: str) -> str:
    source = re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)
    source = re.sub(r"//.*?$", "", source, flags=re.MULTILINE)
    return source


def extract_annotation_bodies(source: str, ann_name: str) -> List[str]:
    mask = masked_java(source)
    bodies: List[str] = []
    pattern = re.compile(r"@(?:[\w.]+\.)?" + re.escape(ann_name) + r"\s*\(")
    for match in pattern.finditer(mask):
        start = mask.find("(", match.start())
        end = end_delimiter(mask, start, "(", ")")
        if end >= 0:
            bodies.append(source[start + 1 : end])
    return bodies


def collect_string_constants(java_files: List[Path]) -> Dict[str, str]:
    raw_consts: Dict[Tuple[str, str], str] = {}
    for path in java_files:
        try:
            txt = strip_comments(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        cls_m = re.search(r"\b(?:class|interface|enum|record)\s+(\w+)", txt)
        if not cls_m:
            continue
        cls_name = cls_m.group(1)
        for m in re.finditer(
            r"\bpublic\s+static\s+final\s+String\s+(\w+)\s*=\s*([^;]+);",
            txt,
        ):
            raw_consts[(cls_name, m.group(1))] = m.group(2).strip()

    const_map: Dict[str, str] = {}
    unique_unqualified: Dict[str, Optional[str]] = {}
    for _ in range(6):
        progressed = False
        for (cls_name, key), expr in raw_consts.items():
            full_key = f"{cls_name}.{key}"
            if full_key in const_map:
                continue
            parts = [p.strip() for p in expr.split("+")]
            resolved: List[str] = []
            ok = True
            for part in parts:
                if len(part) >= 2 and part.startswith('"') and part.endswith('"'):
                    resolved.append(part[1:-1])
                elif f"{cls_name}.{part}" in const_map:
                    resolved.append(const_map[f"{cls_name}.{part}"])
                elif part in const_map:
                    resolved.append(const_map[part])
                elif part in unique_unqualified and unique_unqualified[part] is not None:
                    resolved.append(unique_unqualified[part] or "")
                else:
                    ok = False
                    break
            if ok:
                val = "".join(resolved)
                const_map[full_key] = val
                if key not in unique_unqualified:
                    unique_unqualified[key] = val
                elif unique_unqualified[key] != val:
                    unique_unqualified[key] = None
                progressed = True
        if not progressed:
            break
    for k, v in unique_unqualified.items():
        if v is not None and k not in const_map:
            const_map[k] = v
    return const_map


def _resolve_string_constants(
    source: str, cls_name: Optional[str], const_map: Optional[Dict[str, str]]
) -> str:
    if not const_map:
        return source
    attrs = "id|resourceKey|endpoint|value|path|operationId|evaluationOperationId|surfaceId|previewSurfaceId"
    pattern = re.compile(
        rf"\b({attrs})\s*=\s*([A-Za-z_][\w.]*(?:\.[A-Z0-9_]+)?)\b"
    )

    def _repl(m: re.Match) -> str:
        attr, expr = m.group(1), m.group(2).strip()
        val: Optional[str] = None
        if "." in expr:
            val = const_map.get(expr)
            if val is None:
                parts = expr.split(".")
                if len(parts) >= 2:
                    val = const_map.get(f"{parts[-2]}.{parts[-1]}")
        else:
            if cls_name:
                val = const_map.get(f"{cls_name}.{expr}")
            if val is None and expr.isupper():
                val = const_map.get(expr)
        return f'{attr} = "{val}"' if val is not None else m.group(0)

    return pattern.sub(_repl, source)


def _scan_class_members(source: str) -> Tuple[List[str], List[str]]:
    """Extract top-level field statements and method/constructor headers from a Java class body."""
    cleaned = strip_comments(source)
    class_decl = re.search(r"\b(?:class|record)\s+\w+[^{]*\{", cleaned, re.DOTALL)
    if not class_decl:
        return [], []

    body = cleaned[class_decl.end() :]
    brace_depth = 0
    paren_depth = 0
    current_token: List[str] = []

    top_statements: List[str] = []
    top_headers: List[str] = []
    i = 0
    n = len(body)
    while i < n:
        ch = body[i]
        if ch in "{}" and paren_depth > 0:
            if brace_depth == 0:
                current_token.append(ch)
        elif ch == "{":
            if brace_depth == 0:
                hdr = "".join(current_token).strip()
                if hdr:
                    top_headers.append(hdr)
            brace_depth += 1
            if brace_depth == 1:
                current_token = ["{"]
        elif ch == "}":
            if brace_depth == 0:
                break
            brace_depth -= 1
            if brace_depth == 0:
                current_token = []
        elif ch == "(":
            paren_depth += 1
            if brace_depth == 0:
                current_token.append(ch)
        elif ch == ")":
            if paren_depth > 0:
                paren_depth -= 1
            if brace_depth == 0:
                current_token.append(ch)
        elif ch == ";" and brace_depth == 0 and paren_depth == 0:
            stmt = "".join(current_token).strip()
            if stmt:
                top_statements.append(stmt)
            current_token = []
        else:
            if brace_depth == 0:
                current_token.append(ch)
        i += 1
    return top_statements, top_headers


def _strip_inline_type_annotations(decl_suffix: str) -> str:
    return re.sub(r"@(?:[\w.]+\.)?\w+(?:\s*\([^)]*\))?\s*", "", decl_suffix)


def extract_fields(source: str) -> List[Tuple[str, str, str]]:
    """Extract fields with their preceding annotation block from a Java class body."""
    top_statements, _ = _scan_class_members(source)
    results: List[Tuple[str, str, str]] = []
    vis_re = re.compile(
        r"(?:^|\s)((?:private|protected|public)\s+(?!static\b)(?:final\s+|transient\s+)*)"
    )
    field_re = re.compile(
        r"(?:private|protected|public)\s+(?!static\b)(?:final\s+|transient\s+)*([\w<>?,\s\[\].]+?)\s+(\w+)\s*(?:=.*)?$",
        re.DOTALL,
    )
    for stmt in top_statements:
        vis_m = vis_re.search(stmt)
        if not vis_m:
            continue
        annot_part = stmt[: vis_m.start()].strip()
        prefix_len = vis_m.end() - vis_m.start()
        decl_prefix = stmt[vis_m.start() : vis_m.end()]
        raw_decl_tail = stmt[vis_m.start() + prefix_len :]
        decl_head, eq_sep, decl_init = raw_decl_tail.partition("=")
        decl_suffix = _strip_inline_type_annotations(decl_head) + (eq_sep + decl_init if eq_sep else "")
        m = field_re.search(decl_prefix + decl_suffix)
        if m:
            f_type = m.group(1).strip()
            f_name = m.group(2).strip()
            results.append((f_type, f_name, annot_part))

    return results


def extract_getters(source: str) -> List[Tuple[str, str, str]]:
    """Extract annotated public bean getters with their preceding annotation block."""
    _, top_headers = _scan_class_members(source)
    results: List[Tuple[str, str, str]] = []
    pub_re = re.compile(r"(?:^|\s)(public\s+(?!static\b))")
    getter_sig_re = re.compile(
        r"^([\w<>?,\s\[\].]+?)\s+(?:get([A-Z]\w*)|is([A-Z]\w*))\s*\(\s*\)(?:\s*throws\s+[\w.,\s]+)?$",
        re.DOTALL,
    )
    for hdr in top_headers:
        pub_m = pub_re.search(hdr)
        if not pub_m:
            continue
        annot_part = hdr[: pub_m.start()].strip()
        if not re.search(r"@(?:[\w.]+\.)?(?:UISchema|ResourceReference|Filterable)\b", annot_part):
            continue
        sig_clean = _strip_inline_type_annotations(hdr[pub_m.end() :]).strip()
        gm = getter_sig_re.fullmatch(sig_clean)
        if gm:
            ret_type = gm.group(1).strip()
            raw_prop = gm.group(2) or gm.group(3)
            prop_name = raw_prop[0].lower() + raw_prop[1:]
            results.append((ret_type, prop_name, annot_part))
    return results


def split_top_level_type_args(arg_str: str) -> List[str]:
    args: List[str] = []
    depth = 0
    curr: List[str] = []
    for ch in arg_str:
        if ch == "<":
            depth += 1
            curr.append(ch)
        elif ch == ">":
            depth -= 1
            curr.append(ch)
        elif ch == "," and depth == 0:
            args.append("".join(curr).strip())
            curr = []
        else:
            curr.append(ch)
    if curr:
        args.append("".join(curr).strip())
    return args


def parse_java_file(
    path: Path, const_map: Optional[Dict[str, str]] = None
) -> Optional[JavaClassInfo]:
    try:
        raw_content = path.read_text(encoding="utf-8")
    except Exception:
        return None

    prelim = strip_comments(raw_content)
    cls_name_m = re.search(r"\b(?:class|record)\s+(\w+)", prelim)
    content = _resolve_string_constants(
        raw_content, cls_name_m.group(1) if cls_name_m else None, const_map
    )

    cleaned = strip_comments(content)
    cleaned_header = cleaned
    for _ in range(4):
        cleaned_header = re.sub(
            r"(\bextends\s+[\w.]+)\s*\.\s*([\w.]+)", r"\1.\2", cleaned_header
        )
    class_match = re.search(
        r"\b(?:public\s+|abstract\s+|final\s+)*(?:class|record)\s+(\w+)(?:\s+extends\s+([\w.]+)(?:\s*<([^>{]+)>)?)",
        cleaned_header,
        re.DOTALL,
    )
    if not class_match:
        simple_match = re.search(r"\b(?:class|record)\s+(\w+)", cleaned_header)
        if not simple_match:
            return None
        name = simple_match.group(1)
        superclass = None
        type_args_raw = None
    else:
        name = class_match.group(1)
        superclass = class_match.group(2).split(".")[-1] if class_match.group(2) else None
        type_args_raw = class_match.group(3)

    info = JavaClassInfo(name=name, path=path, content=content, superclass=superclass)
    info.is_entity = "@Entity" in cleaned or "@MappedSuperclass" in cleaned
    info.is_controller = bool(
        superclass
        and superclass
        in {
            "AbstractResourceController",
            "AbstractReadOnlyResourceController",
            "AbstractCollectionCommandResourceController",
            "AbstractResourceQueryController",
        }
    )
    info.is_service = bool(
        superclass
        and (
            superclass in {"AbstractBaseResourceService", "AbstractReadOnlyResourceService"}
            or superclass.endswith("ResourceService")
        )
        and type_args_raw
    )

    if "@ApiResource" in cleaned:
        rk_match = re.search(r'resourceKey\s*=\s*"([^"]+)"', cleaned)
        if rk_match:
            info.resource_key = rk_match.group(1)

    if (info.is_controller or info.resource_key) and type_args_raw:
        info.controller_type_args = split_top_level_type_args(type_args_raw)

    if info.is_service and type_args_raw:
        info.service_type_args = split_top_level_type_args(type_args_raw)

    info.fields = extract_fields(content)
    info.getters = extract_getters(content)
    return info


def get_all_fields_with_inheritance(
    cls_name: str, classes: Dict[str, JavaClassInfo]
) -> List[Tuple[str, str, str]]:
    visited: Set[str] = set()
    chain: List[JavaClassInfo] = []
    curr = classes.get(cls_name)
    while curr and curr.name not in visited:
        visited.add(curr.name)
        chain.append(curr)
        curr = classes.get(curr.superclass) if curr.superclass else None

    merged: Dict[str, Tuple[str, str, str]] = {}
    for c in reversed(chain):
        for f_type, f_name, f_annot in c.fields:
            merged[f_name] = (f_type, f_name, f_annot)
        for g_type, g_name, g_annot in c.getters:
            if g_name in merged:
                old_type, _, old_annot = merged[g_name]
                merged[g_name] = (old_type, g_name, (old_annot + "\n" + g_annot).strip())
            elif re.search(r"@(?:[\w.]+\.)?(?:UISchema|ResourceReference)\b", g_annot):
                merged[g_name] = (g_type, g_name, g_annot)
    return list(merged.values())


def entity_field_covered_in_dto(entity_field: str, entity_type: str, dto_fields: Set[str]) -> bool:
    return entity_field in dto_fields


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit Praxis Java resource completeness, Quick View readiness, and editorial quality."
    )
    parser.add_argument("project_dir", type=Path, help="Path to the Java host project root")
    parser.add_argument("--strict", action="store_true", help="Explicit gate mode; failures always exit with code 1")
    parser.add_argument(
        "--min-dto-coverage",
        type=float,
        default=100.0,
        help="Minimum reading coverage %% (default: 100; cannot weaken accountability)",
    )
    parser.add_argument("--require-runtime-evidence", action="store_true", help="Also require fresh hashed receipts for operational/consumer/parity gates")
    parser.add_argument("--evidence-manifest", type=Path, default=None, help="Default: <host>/docs/evidence/runtime-gates.json")
    args = parser.parse_args()
    if args.min_dto_coverage != 100.0:
        parser.error("The governed completeness gate requires exactly 100% coverage.")

    src_main = args.project_dir / "src" / "main" / "java"
    if not src_main.exists():
        print(f"ERROR: Could not find {src_main}", file=sys.stderr)
        return 2

    java_files = sorted(src_main.rglob("*.java"))
    const_map = collect_string_constants(java_files)
    classes: Dict[str, JavaClassInfo] = {}
    for java_file in java_files:
        info = parse_java_file(java_file, const_map)
        if info:
            classes[info.name] = info

    controllers = [c for c in classes.values() if c.is_controller and c.controller_type_args]
    services = [c for c in classes.values() if c.is_service and c.service_type_args]
    entities = [c for c in classes.values() if "@Entity" in c.content]
    published_entities = {svc.service_type_args[0] for svc in services
                          if any(ctrl.controller_type_args[0] == svc.service_type_args[1]
                                 for ctrl in controllers) and len(svc.service_type_args) >= 2}
    if not controllers:
        print("ERROR: no supported resource controllers found; nothing was proven.",file=sys.stderr)
        return 2

    resources = {c.resource_key: c for c in classes.values() if c.resource_key and c.controller_type_args}
    read_surfaces = {}
    for key, controller in resources.items():
        read_surfaces[key] = set()
        for annotation in extract_annotation_bodies(strip_comments(controller.content), "UiSurface"):
            if re.search(r"SurfaceKind\.(?:VIEW|READ_PROJECTION)\b", annotation):
                surface_id = re.search(r'id\s*=\s*"([^"]+)"', annotation)
                if surface_id:
                    read_surfaces[key].add(surface_id.group(1))

    print("# Praxis Resource Completeness, Quick View & Editorial Quality Audit")
    print(f"- **Project**: `{args.project_dir.resolve()}`")
    print(f"- **Mapped JPA Entities**: {len(entities)}")
    print(f"- **Resource Controllers**: {len(controllers)}\n")
    print("- **Scope**: static source evidence; not HTTP, concurrency, parity or runtime approval. N+1 requires cold full-query/page/cursor/export measurements; this source audit cannot certify it.\n")

    print("## 1. Resource & Capability Scorecard")
    print(
        "| Resource (`resourceKey`) | Entity | BizCols | RespCols | Cov % | Accounted writes | FilterCols | FilterOps | `@QuickFilter` | QuickViewCols | RichIdentity | `@ResourceRef` (`preview`) | `@UiSurface` | `@WorkflowAction` | `@ResourceIntent` | `@ResourceFact` | `MicroViz` | `UiAnalytics` | `ReactiveDet` | BulkEditable | BulkOps | EditorialIssues | Status |"
    )
    print("|---|---|---:|---:|---:|---:|---:|---|---:|---:|:---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")

    failures: List[str] = []
    unmapped_details: List[Tuple[str, str, List[str]]] = []
    editorial_details: List[Tuple[str, List[str]]] = []

    for ctrl in controllers:
        t_args = ctrl.controller_type_args
        if len(t_args) >= 5:
            resp_dto_name, _, filter_dto_name, create_dto_name, update_dto_name = t_args[:5]
        elif len(t_args) == 3:
            resp_dto_name, _, filter_dto_name = t_args
            create_dto_name, update_dto_name = "", ""
        else:
            failures.append(f"{ctrl.name}: unsupported generic resource binding")
            continue

        matched_svc = next(
            (
                s
                for s in services
                if len(s.service_type_args) >= 2 and s.service_type_args[1] == resp_dto_name
            ),
            None,
        )
        entity_name = matched_svc.service_type_args[0] if matched_svc else ""
        entity_all_fields = (
            get_all_fields_with_inheritance(entity_name, classes) if entity_name else []
        )
        resp_all_fields = (
            get_all_fields_with_inheritance(resp_dto_name, classes) if resp_dto_name else []
        )
        create_all_fields = (
            get_all_fields_with_inheritance(create_dto_name, classes) if create_dto_name else []
        )
        update_all_fields = (
            get_all_fields_with_inheritance(update_dto_name, classes) if update_dto_name else []
        )
        filter_all_fields = (
            get_all_fields_with_inheritance(filter_dto_name, classes) if filter_dto_name else []
        )

        entity_biz_fields: List[Tuple[str, str]] = []
        for f_type, f_name, f_annot in entity_all_fields:
            if technical_or_mirrored(f_name, f_annot, AUDIT_EXCLUDED_ENTITY_FIELDS):
                continue
            entity_biz_fields.append((f_type, f_name))

        resp_fields = {
            f_name for _, f_name, _ in resp_all_fields if f_name not in AUDIT_EXCLUDED_ENTITY_FIELDS
        }
        create_fields = {name for _, name, _ in create_all_fields}
        update_fields = {name for _, name, _ in update_all_fields}

        covered_count = 0
        missing_fields: List[str] = []
        for f_type, f_name in entity_biz_fields:
            if entity_field_covered_in_dto(f_name, f_type, resp_fields):
                covered_count += 1
            else:
                missing_fields.append(f_name)

        total_ent_biz = len(entity_biz_fields)
        coverage_pct = (covered_count / total_ent_biz * 100.0) if total_ent_biz > 0 else 100.0

        filterable_count = 0
        filter_ops: Set[str] = set()
        for _, f_name, f_annot in filter_all_fields:
            if "@Filterable" in f_annot:
                filterable_count += 1
                op_match = re.search(r"operation\s*=\s*(?:FilterOperation\.)?(\w+)", f_annot)
                filter_ops.add(op_match.group(1) if op_match else "EQUAL")

        # Quick View & Editorial checks across ResponseDTO + base DTO + FilterDTO
        quick_view_cols = 0
        res_ref_count = 0
        res_ref_preview_count = 0
        res_editorial_issues: List[str] = []

        for f_type, f_name, f_annot in resp_all_fields:
            if re.search(r"quickViewVisible\s*=\s*true", f_annot):
                quick_view_cols += 1
            if re.search(r"@(?:[\w.]+\.)?ResourceReference\b", f_annot):
                res_ref_count += 1
                if re.search(r'previewSurfaceId\s*=\s*"[^"]+"', f_annot):
                    res_ref_preview_count += 1
            for ui_body in extract_annotation_bodies(f_annot, "UISchema"):
                lbl_match = re.search(r'label\s*=\s*"([^"]+)"', ui_body)
                if lbl_match:
                    lbl = lbl_match.group(1).strip()
                    if len(lbl) > 36 or lbl.endswith("."):
                        res_editorial_issues.append(
                            f"{resp_dto_name}.{f_name}: label looks like a sentence/description ('{lbl}')"
                        )
            simple_type = f_type if "<" in f_type else f_type.split(".")[-1]
            if simple_type in {"LocalDate", "LocalDateTime"} and "@UISchema" in f_annot:
                if "controlType" not in f_annot and "preset" not in f_annot:
                    res_editorial_issues.append(
                        f"{resp_dto_name}.{f_name} ({f_type}): @UISchema missing explicit controlType=DATE_PICKER"
                    )

        for f_type, f_name, f_annot in filter_all_fields:
            for ui_body in extract_annotation_bodies(f_annot, "UISchema"):
                lbl_match = re.search(r'label\s*=\s*"([^"]+)"', ui_body)
                if lbl_match:
                    lbl = lbl_match.group(1).strip()
                    if len(lbl) > 36 or lbl.endswith("."):
                        res_editorial_issues.append(
                            f"{filter_dto_name}.{f_name}: label looks like a sentence/description ('{lbl}')"
                        )

        foreign_keys = relationship_key_fields(entity_all_fields)
        checked_ui = set()
        for field_type, field_name, annotations in resp_all_fields + create_all_fields + update_all_fields + filter_all_fields:
            signature = (field_type, field_name, annotations)
            if signature in checked_ui:
                continue
            checked_ui.add(signature)
            res_editorial_issues.extend(presentation_issues(field_type, field_name, annotations, foreign_keys))
        display_fields = relationship_display_fields(entity_name, entity_all_fields, classes)
        for display in display_fields:
            annotation = next((a for _, n, a in resp_all_fields if n == display), "")
            if not re.search(r"@(?:[\w.]+\.)?ResourceReference\b", annotation):
                res_editorial_issues.append(f"{display}: mapped relationship display lacks @ResourceReference")

        related_class_names = {
            ctrl.name,
            matched_svc.name if matched_svc else "",
            resp_dto_name,
            create_dto_name,
            update_dto_name,
            filter_dto_name,
        }
        for dto_n in (resp_dto_name, create_dto_name, update_dto_name, filter_dto_name):
            c_obj = classes.get(dto_n)
            if c_obj and c_obj.superclass:
                related_class_names.add(c_obj.superclass)

        combined_sources = "\n".join(
            classes[n].content for n in related_class_names if n and n in classes
        )
        identities = [extract_annotation_bodies(source, "ResourceIdentity")
                      for source in (ctrl.content, classes[resp_dto_name].content if resp_dto_name in classes else "")]
        has_rich_identity = all(
            identity_bodies
            and any(
                re.search(r'subtitleField\s*=\s*"[^"]+"', body)
                and re.search(r'metadataFields\s*=\s*\{?\s*"[^"]+"', body)
                for body in identity_bodies
            )
            for identity_bodies in identities
        )
        has_read_surface = any(
            re.search(r"SurfaceKind\.(?:VIEW|READ_PROJECTION)\b", body)
            for body in extract_annotation_bodies(combined_sources, "UiSurface")
        )
        quick_filter_count = len(re.findall(r"@(?:[\w.]+\.)?QuickFilter\b", combined_sources))
        ui_surface_count = len(re.findall(r"@(?:[\w.]+\.)?UiSurface\b", combined_sources))
        workflow_action_count = len(
            re.findall(r"@(?:[\w.]+\.)?WorkflowAction\b", combined_sources)
        )
        resource_intent_count = len(
            re.findall(r"@(?:[\w.]+\.)?ResourceIntent\b", combined_sources)
        )
        bulk_editable_count, bulk_operation_count, bulk_issues = bulk_source_summary(ctrl.content, update_all_fields)
        resource_fact_count = len(re.findall(r"@(?:[\w.]+\.)?ResourceFact\b", combined_sources))
        micro_viz_count = len(micro_visualization_properties(resp_dto_name, classes, resp_all_fields))
        ui_analytics_count = len(re.findall(r"@(?:[\w.]+\.)?AnalyticsProjection\b", combined_sources))
        reactive_det_count = reactive_determination_count(ctrl.content, classes)
        res_editorial_issues.extend(resource_fact_editorial_issues(ctrl.content, ctrl.name))
        res_editorial_issues.extend(dto_table_visibility_issues(resp_dto_name, resp_all_fields))
        for proj_dto in set(re.findall(r'\bResponseEntity<\s*([\w.]+)\s*>', strip_comments(ctrl.content))):
            proj_short = proj_dto.split(".")[-1]
            if proj_short != resp_dto_name and proj_short in classes:
                res_editorial_issues.extend(dto_table_visibility_issues(proj_short, get_all_fields_with_inheritance(proj_short, classes)))

        mapper_n_plus_one = False
        for info in classes.values():
            if re.search(r"\bResourceMapper\s*<\s*" + re.escape(entity_name) + r"\s*,", info.content):
                if re.search(r"\b(?:createQuery|createNativeQuery)\s*\(", strip_comments(info.content)):
                    mapper_n_plus_one = True

        res_label = ctrl.resource_key or ctrl.name
        row_issues: List[str] = []
        if not entity_name or not entity_biz_fields:
            row_issues.append("Unresolved entity/business-column binding")
        writable = mapped_input_fields(entity_name, create_fields | update_fields, classes)
        commands = command_fields(ctrl, entity_name, classes)
        readonly = {name for _, name, annotation in resp_all_fields
                    if re.search(r'readOnly\s*=\s*true|accessMode\s*=\s*(?:Schema\.)?AccessMode\.READ_ONLY', annotation)}
        writable_resource = bool(create_dto_name or update_dto_name)
        orphaned = [name for _, name in entity_biz_fields
                    if name not in writable and not (name in readonly and name in commands)] if writable_resource else []
        accounted_writes = f"{total_ent_biz-len(orphaned)}/{total_ent_biz}" if writable_resource else "N/A (read-only)"
        if orphaned:
            row_issues.append("Unaccounted business writes: " + ", ".join(orphaned))
        print(f"<!-- {res_label}: functional-accountability={total_ent_biz-len(orphaned)}/{total_ent_biz}; command-managed={','.join(sorted(commands)) or 'none'} -->")

        if total_ent_biz > 0 and coverage_pct < max(100.0, args.min_dto_coverage):
            row_issues.append(f"DTO coverage {coverage_pct:.1f}% < {args.min_dto_coverage:.0f}%")
        if total_ent_biz >= 8 and filterable_count < 5:
            row_issues.append(f"Only {filterable_count} @Filterable")
        if total_ent_biz >= 8 and len(filter_ops) < 3:
            row_issues.append(f"Low FilterOperation diversity ({len(filter_ops)})")
        if quick_filter_count < 2:
            row_issues.append(f"Only {quick_filter_count} @QuickFilter")
        identity_fields = set(re.findall(r'(?:titleField|subtitleField)\s*=\s*"([^"]+)"', combined_sources))
        for _, field_name, annotations in resp_all_fields:
            if field_name in identity_fields and re.search(r'quickViewVisible\s*=\s*true', annotations):
                row_issues.append(f"Quick View repeats identity field: {field_name}")

        all_identity_summary_fields = set(
            re.findall(r'(?:keyField|titleField|subtitleField|avatarField)\s*=\s*"([^"]+)"', combined_sources)
        )
        for m in re.finditer(r'metadataFields\s*=\s*(?:\{([^}]*)\}|"([^"]+)")', combined_sources):
            if m.group(1) is not None:
                all_identity_summary_fields.update(re.findall(r'"([^"]+)"', m.group(1)))
            elif m.group(2):
                all_identity_summary_fields.add(m.group(2))
        available_quick_view_candidates = {
            name
            for _, name, _ in resp_all_fields
            if name not in all_identity_summary_fields and name not in AUDIT_EXCLUDED_ENTITY_FIELDS
        }
        min_quick_view = min(4, len(available_quick_view_candidates)) if available_quick_view_candidates else 4

        if not min_quick_view <= quick_view_cols <= 8:
            row_issues.append(f"QuickView field count outside 4..8: {quick_view_cols}")
        if not has_rich_identity:
            row_issues.append("Shallow @ResourceIdentity (missing subtitleField/metadataFields)")
        reference_targets = {typ for typ, _, annot in entity_all_fields
                             if typ in published_entities and re.search(r"@(?:ManyToOne|OneToOne)\b", annot)}
        if reference_targets and res_ref_count < 1:
            row_issues.append("0 @ResourceReference (title/FK fields not wired for Quick View 360)")
        elif res_ref_preview_count < res_ref_count:
            row_issues.append(f"@ResourceReference missing previewSurfaceId ({res_ref_preview_count}/{res_ref_count})")
        title = re.search(r'titleField\s*=\s*"([^"]+)"', combined_sources)
        title_annotations = next((annotations for _, field_name, annotations in resp_all_fields
                                  if title and field_name == title.group(1)), "")
        if not any(
            re.search(r'resourceKey\s*=\s*"' + re.escape(ctrl.resource_key or "") + r'"', body)
            for body in extract_annotation_bodies(title_annotations, "ResourceReference")
        ):
            row_issues.append("Resource title lacks an explicit self reference")
        for target_entity in reference_targets:
            target_keys = {key for key, controller in resources.items()
                           if any(svc.service_type_args[0] == target_entity and
                                  svc.service_type_args[1] == controller.controller_type_args[0]
                                  for svc in services)}
            if not any(key in annotations for _, _, annotations in resp_all_fields
                       if re.search(r"@(?:[\w.]+\.)?ResourceReference\b", annotations) for key in target_keys):
                row_issues.append(f"Missing published relationship reference: {target_entity}")
        # A reference must resolve to a real resource and its declared item read surface.
        for _, field_name, annotations in resp_all_fields:
            for reference in extract_annotation_bodies(annotations, "ResourceReference"):
                values = dict(re.findall(r'(resourceKey|surfaceId|previewSurfaceId)\s*=\s*"([^"]+)"', reference))
                target = values.get("resourceKey", "")
                if target not in resources:
                    row_issues.append(f"Unresolved reference target: {field_name} -> {target}")
                else:
                    for attribute in ("surfaceId", "previewSurfaceId"):
                        if values.get(attribute) not in read_surfaces.get(target, set()):
                            row_issues.append(f"Unresolved reference surface: {field_name}.{attribute} -> {target}/{values.get(attribute, '')}")
        if not has_read_surface:
            row_issues.append("Missing READ_PROJECTION/VIEW @UiSurface for Quick View 360")
        if mapper_n_plus_one:
            row_issues.append("Explicit query inside ResourceMapper (runtime query-count proof is required separately)")
        if (
            ui_surface_count + workflow_action_count + resource_intent_count + resource_fact_count
        ) < 1:
            row_issues.append("0 semantic capabilities")
        if res_editorial_issues:
            row_issues.append(f"{len(res_editorial_issues)} @UISchema editorial issues")

        row_issues.extend(bulk_issues)
        if writable_resource and total_ent_biz >= 15 and (bulk_editable_count < 1 or bulk_operation_count < 1):
            row_issues.append(f"Enterprise mutable resource (>=15 biz cols) missing @BulkEditable/@BulkOperation ({bulk_editable_count}/{bulk_operation_count})")
        if writable_resource and total_ent_biz >= 15 and micro_viz_count < 1:
            row_issues.append("Enterprise mutable resource (>=15 biz cols) missing @MicroVisualization")
        if writable_resource and total_ent_biz >= 15 and ui_analytics_count < 1:
            row_issues.append("Enterprise mutable resource (>=15 biz cols) missing @UiAnalytics/@AnalyticsProjection")
        if writable_resource and total_ent_biz >= 15 and reactive_det_count < 1:
            row_issues.append("Enterprise mutable resource (>=15 biz cols) missing ReactiveDeterminationDefinitionProvider")
        status_str = "PASS" if not row_issues else "FAIL (" + "; ".join(row_issues) + ")"
        if row_issues:
            failures.append(f"{res_label}: {status_str}")
        if missing_fields:
            unmapped_details.append((res_label, entity_name, missing_fields))
        if res_editorial_issues:
            editorial_details.append((res_label, res_editorial_issues))

        if not reference_targets and res_ref_count == 0:
            print(f"<!-- {res_label}: resource-reference=N/A (no association to another published entity) -->")
        ops_str = f"{len(filter_ops)} ops"
        rich_id_str = "YES" if has_rich_identity else "NO"
        print(
            f"| `{res_label}` | `{entity_name}` | {total_ent_biz} | {len(resp_fields)} | {coverage_pct:.1f}% | {accounted_writes} | {filterable_count} | {ops_str} | {quick_filter_count} | {quick_view_cols} | {rich_id_str} | {res_ref_count} ({res_ref_preview_count}) | {ui_surface_count} | {workflow_action_count} | {resource_intent_count} | {resource_fact_count} | {micro_viz_count} | {ui_analytics_count} | {reactive_det_count} | {bulk_editable_count} | {bulk_operation_count} | {len(res_editorial_issues)} | **{status_str}** |"
        )

    lookup_issues = entity_lookup_descriptor_issues(classes)
    if lookup_issues:
        editorial_details.append(("OptionSources / EntityLookupDescriptor", lookup_issues))
        for li in lookup_issues:
            failures.append(f"OptionSources: FAIL ({li})")

    det_issues = reactive_determination_issues(classes)
    if det_issues:
        editorial_details.append(("ReactiveDeterminations", det_issues))
        for di in det_issues:
            failures.append(f"ReactiveDeterminations: FAIL ({di})")

    if unmapped_details:
        print("\n## 2. Unmapped Entity Business Columns (Entity -> ResponseDTO Gaps)")
        for res_label, ent_name, missing in unmapped_details:
            print(
                f"- **`{res_label}` (`{ent_name}`)** — {len(missing)} unmapped columns: `{', '.join(missing)}`"
            )

    if editorial_details:
        print("\n## 3. @UISchema Editorial & Metadata Quality Issues")
        for res_label, issues in editorial_details:
            print(f"- **`{res_label}`** ({len(issues)} issues):")
            for iss in issues[:12]:
                print(f"  - `{iss}`")
            if len(issues) > 12:
                print(f"  - ... and {len(issues) - 12} more")

    if args.require_runtime_evidence:
        manifest = args.evidence_manifest or args.project_dir / "docs/evidence/runtime-gates.json"
        issues = runtime_evidence_issues(args.project_dir.resolve(), manifest)
        print("\n## Operational Evidence Receipts")
        print("Hashed receipts are checked for freshness; independent review remains required.")
        failures.extend(issues)
        for issue in issues:
            print("- " + issue)

    if failures:
        print(
            f"\n## 4. Verdict: FAILED ({len(failures)} structural or operational gate failure(s))"
        )
        for f in failures:
            print(f"- [x] {f}")
        return 1
    else:
        if args.require_runtime_evidence:
            print("\n## 4. OVERALL STATUS: PASS (static + operational runtime evidence)")
            print("Receipt integrity and source freshness verified; independent architectural review remains required.")
        else:
            print(
                "\n## 4. Verdict: STATIC PASS (source gates satisfied; runtime and architectural review still required)"
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
