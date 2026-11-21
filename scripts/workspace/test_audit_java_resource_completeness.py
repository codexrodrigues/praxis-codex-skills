"""Regression proofs for the canonical static audit; no product DTO enrichment."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location("resource_audit_cli",ROOT/"audit-java-resource-completeness.py")
audit=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=audit
spec.loader.exec_module(audit)
from java_resource_audit import (
    technical_or_mirrored,
    command_fields,
    mapped_input_fields,
    presentation_issues,
    relationship_key_fields,
    relationship_display_fields,
    source_fingerprint,
    runtime_evidence_issues,
    RUNTIME_GATES,
    bulk_source_summary,
    resource_fact_editorial_issues,
    dto_table_visibility_issues,
    entity_lookup_descriptor_issues,
    micro_visualization_properties,
    reactive_determination_count,
    reactive_determination_issues,
)


def info(name,content,fields=()):
    return SimpleNamespace(name=name,content=content,fields=fields)


class CompletenessRegression(unittest.TestCase):
    def fixture_audit(self,write_command=False,extra_args=(),strict=True,reference="",read_only=False,runtime_status=None):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp,"src/main/java");root.mkdir(parents=True)
            names=[f"field{i}" for i in range(8)]
            base=" ".join((('@ResourceReference(resourceKey="test.items",surfaceId="view",previewSurfaceId="view") ' if n=="field0" else "") + f'@UISchema(quickViewVisible={str(n not in names[:2]).lower()},quickViewOrder={names.index(n)+1}) private String {n};') for n in names)
            entity=" ".join(f'@Column private String {n};' for n in names)
            filters=" ".join(f'@UISchema(label="Filter") @Filterable(operation=FilterOperation.{op}) private String filter{i};' for i,op in enumerate(["LIKE","EQUAL","IN","LIKE","EQUAL"]))
            assignments="".join(f'entity.setField{i}(dto.getField{i}());' for i in range(8))
            sources={
                "Item":f"@Entity public class Item {{ @Id private Long id;{entity} @Column private LocalDate deadline; }}",
                "Base":f"public class Base {{{base}}}",
                "Response":'@ResourceIdentity(titleField="field0",subtitleField="field1",metadataFields={"field2"}) public class Response extends Base {@Schema(accessMode=Schema.AccessMode.READ_ONLY) @UISchema(label="Deadline",type=FieldDataType.DATE,controlType=FieldControlType.DATE_PICKER,icon="event") private LocalDate deadline;}',
                "Create":"public class Create extends Base {}",
                "Update":"public class Update extends Base {}",
                "Filter":f"public class Filter {{{filters}}}",
                "Mapper":f"public class Mapper implements ResourceMapper<Item,Response,Create,Update,Long> {{public void apply(){{{assignments}}}}}",
                "Service":"@Service public class Service extends AbstractBaseResourceService<Item,Response,Long,Filter,Create,Update> {}",
                "Controller":'@ApiResource(identity=@ResourceIdentity(titleField="field0",subtitleField="field1",metadataFields={"field2"}),resourceKey="test.items",quickFilters={@QuickFilter(id="a"),@QuickFilter(id="b")}) public class Controller extends AbstractResourceController<Response,Long,Filter,Create,Update> {private final Commands commands; @GetMapping("/{id}/view") @UiSurface(id="view",kind=SurfaceKind.READ_PROJECTION) public Response view(){return null;} @WorkflowAction(id="close") @PostMapping("/actions/close") public Response close(){return commands.close();}}',
                "Commands":"public class Commands {public Response close(){Item e=load();"+("e.setDeadline(dto.deadline());" if write_command else "")+"return null;}}",
            }
            if read_only:
                sources["Controller"] = sources["Controller"].replace("AbstractResourceController<Response,Long,Filter,Create,Update>", "AbstractReadOnlyResourceController<Response,Long,Filter>")
                sources["Service"] = sources["Service"].replace("AbstractBaseResourceService<Item,Response,Long,Filter,Create,Update>", "AbstractReadOnlyResourceService<Item,Response,Long,Filter>")
            for name,source in sources.items():Path(root,name+".java").write_text(source.replace("private LocalDate deadline;", reference+" private LocalDate deadline;") if name=="Response" else source,encoding="utf-8")
            if runtime_status is not None:
                import json, hashlib
                project = Path(tmp)
                evidence = project / "docs/evidence"
                evidence.mkdir(parents=True)
                receipt = evidence / "proof.txt"
                receipt.write_text("Fixture runtime receipt", encoding="utf-8")
                artifact = {"path": "docs/evidence/proof.txt", "sha256": hashlib.sha256(receipt.read_bytes()).hexdigest()}
                gates = {name: {"status": "pass", "artifacts": [artifact]} for name in RUNTIME_GATES}
                gates["http"]["status"] = runtime_status
                (evidence / "runtime-gates.json").write_text(json.dumps({"sourceSha256": source_fingerprint(project), "gates": gates}), encoding="utf-8")
            return subprocess.run([sys.executable,str(ROOT/"audit-java-resource-completeness.py"),tmp,*(["--strict"] if strict else []),*extra_args],capture_output=True,text=True)

    def test_default_gate_also_returns_failure(self):
        result=self.fixture_audit(strict=False)
        self.assertEqual(result.returncode,1,result.stdout+result.stderr)

    def test_cli_rejects_readonly_column_without_command_even_at_full_reading_coverage(self):
        result=self.fixture_audit()
        self.assertEqual(result.returncode,1,result.stdout+result.stderr)
        self.assertIn("Unaccounted business writes: deadline",result.stdout)

    def test_cli_accepts_real_bound_writer_but_only_claims_static_pass(self):
        result=self.fixture_audit(True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertIn("STATIC PASS",result.stdout)
        self.assertIn("functional-accountability=9/9",result.stdout)

    def test_cli_labels_verified_runtime_receipts_separately_from_static_only(self):
        result = self.fixture_audit(True, extra_args=("--require-runtime-evidence",), runtime_status="pass")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OVERALL STATUS: PASS (static + operational runtime evidence)", result.stdout)
        self.assertIn("independent architectural review remains required", result.stdout)

    def test_cli_does_not_claim_overall_pass_for_pending_runtime_gate(self):
        result = self.fixture_audit(True, extra_args=("--require-runtime-evidence",), runtime_status="pending")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("http: pending", result.stdout)
        self.assertNotIn("OVERALL STATUS: PASS", result.stdout)

    def test_reference_cannot_point_to_a_missing_resource(self):
        result=self.fixture_audit(True,reference='@ResourceReference(resourceKey="absent",surfaceId="view",previewSurfaceId="view")')
        self.assertEqual(result.returncode,1,result.stdout+result.stderr)
        self.assertIn("Unresolved reference target",result.stdout)

    def test_reference_cannot_point_to_an_undeclared_surface(self):
        result=self.fixture_audit(True,reference='@ResourceReference(resourceKey="test.items",surfaceId="invented",previewSurfaceId="invented")')
        self.assertEqual(result.returncode,1,result.stdout+result.stderr)
        self.assertIn("Unresolved reference surface",result.stdout)

    def test_real_self_reference_is_accepted(self):
        result=self.fixture_audit(True,reference='@ResourceReference(resourceKey="test.items",surfaceId="view",previewSurfaceId="view")')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_read_only_resource_does_not_require_mutation_handlers(self):
        result=self.fixture_audit(read_only=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertIn("N/A (read-only)",result.stdout)

    def test_date_preset_does_not_replace_explicit_presentation(self):
        self.assertTrue(presentation_issues("LocalDate","when",'@UISchema(preset=Preset.DATE)'))

    def test_amount_requires_explicit_semantics_but_is_not_assumed_currency(self):
        self.assertEqual(presentation_issues("BigDecimal","ratio",'@UISchema(type=FieldDataType.NUMBER,controlType=FieldControlType.NUMERIC_TEXT_BOX,icon="percent")'),[])
        self.assertEqual(len(presentation_issues("BigDecimal","amount",'@UISchema(label="Amount")')),3)

    def test_named_relationship_lookup_is_required(self):
        invalid='@UISchema(type=FieldDataType.TEXT,controlType=FieldControlType.ENTITY_LOOKUP,icon="badge",endpoint="/api/items/options/filter")'
        self.assertIn("named RESOURCE_ENTITY",presentation_issues("Long","ownerId",invalid,{"ownerId"})[0])
        valid=invalid.replace('/api/items/options/filter','/api/items/option-sources/item/options/filter')
        self.assertEqual(presentation_issues("Long","ownerId",valid,{"ownerId"}),[])

    def test_raw_joined_foreign_key_cannot_be_a_generic_input(self):
        annotations='@UISchema(type=FieldDataType.TEXT,controlType=FieldControlType.INPUT,icon="badge")'
        self.assertTrue(presentation_issues("Long","ownerId",annotations,{"ownerId"}))

    def test_foreign_keys_come_from_join_column_pairs_not_property_suffixes(self):
        fields=[("Owner","owner",'@ManyToOne @JoinColumn(name="owner_key",insertable=false,updatable=false)'),("Long","ownerKey",'@Column(name="owner_key")'),("String","notAForeignId",'@Column(name="free_code")')]
        self.assertEqual(relationship_key_fields(fields),{"ownerKey"})

    def test_date_interval_is_not_a_scalar_picker(self):
        self.assertTrue(presentation_issues("List<LocalDate>","period",'@UISchema(controlType=FieldControlType.DATE_PICKER)'))
        self.assertEqual(presentation_issues("List<LocalDate>","period",'@UISchema(controlType=FieldControlType.DATE_RANGE)'),[])

    def test_relation_display_is_found_from_mapper_access_not_field_label(self):
        mapper=info("Mapper","class Mapper implements ResourceMapper<Item,R,C,U,Long>{R toResponse(Item entity){R dto=new R();dto.setUnitName(entity.getLocation()==null?null:entity.getLocation().getName());return dto;}}")
        self.assertEqual(relationship_display_fields("Item",[("Location","location","@ManyToOne")],{"Mapper":mapper}),{"unitName"})

    def test_runtime_evidence_is_fail_closed_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            project=Path(tmp)
            self.assertTrue(runtime_evidence_issues(project,project/"missing.json"))

    def test_runtime_evidence_na_requires_reason_and_cannot_hide_a_pending_gate(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            project=Path(tmp); manifest=project/"evidence.json"
            gates={name:{"status":"not-applicable","reason":"No such published feature"} for name in RUNTIME_GATES}
            manifest.write_text(json.dumps({"sourceSha256":source_fingerprint(project),"gates":gates}))
            self.assertEqual(runtime_evidence_issues(project,manifest),[])
            gates["http"]={"status":"pending"}
            manifest.write_text(json.dumps({"sourceSha256":source_fingerprint(project),"gates":gates}))
            self.assertIn("http: pending",runtime_evidence_issues(project,manifest))
            gates["http"]={"status":"not-applicable"}
            manifest.write_text(json.dumps({"sourceSha256":source_fingerprint(project),"gates":gates}))
            self.assertTrue(runtime_evidence_issues(project,manifest))

    def test_runtime_evidence_source_change_invalidates_receipt(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            project=Path(tmp);src=project/"src";src.mkdir();(src/"A.java").write_text("class A {}")
            manifest=project/"evidence.json"
            gates={name:{"status":"not-applicable","reason":"No such published feature"} for name in RUNTIME_GATES}
            manifest.write_text(json.dumps({"sourceSha256":source_fingerprint(project),"gates":gates}))
            (src/"A.java").write_text("class A { int changed; }")
            self.assertIn("Runtime evidence is stale for the current host sources",runtime_evidence_issues(project,manifest))

    def test_runtime_pass_needs_actual_artifact_hashes(self):
        import json, hashlib
        with tempfile.TemporaryDirectory() as tmp:
            project=Path(tmp);manifest=project/"evidence.json";artifact=project/"result.txt";artifact.write_text("pass")
            gates={name:{"status":"not-applicable","reason":"No such published feature"} for name in RUNTIME_GATES}
            gates["http"]={"status":"pass","artifacts":[{"path":"result.txt","sha256":hashlib.sha256(artifact.read_bytes()).hexdigest()}]}
            data={"sourceSha256":source_fingerprint(project),"gates":gates};manifest.write_text(json.dumps(data))
            self.assertEqual(runtime_evidence_issues(project,manifest),[])
            artifact.write_text("changed");self.assertIn("http: artifact hash mismatch",runtime_evidence_issues(project,manifest))

    def test_comments_and_strings_do_not_count_as_writes(self):
        ctrl=info("Controller",'class Controller { @WorkflowAction(id="x") @PostMapping("/actions/x") public void x(){Item e=load();log("e.setDeadline(1)"); /* e.setDeadline(2); */} }')
        self.assertEqual(command_fields(ctrl,"Item",{"Controller":ctrl}),set())

    def test_partly_writable_join_is_not_discarded(self):
        annotations="@ManyToOne @JoinColumns({@JoinColumn(insertable=false,updatable=false),@JoinColumn(insertable=true,updatable=false)})"
        self.assertFalse(technical_or_mirrored("owner",annotations,set()))

    def test_only_readonly_mirrored_relations_are_excluded(self):
        self.assertTrue(technical_or_mirrored("owner","@ManyToOne @JoinColumn(insertable=false,updatable=false)",set()))
        self.assertFalse(technical_or_mirrored("owner","@ManyToOne @JoinColumn",set()))
        self.assertFalse(technical_or_mirrored("version","@Column",{"version"}))
        self.assertTrue(technical_or_mirrored("revision","@Version @Column",set()))

    def test_similar_labels_never_cover_a_column(self):
        self.assertFalse(audit.entity_field_covered_in_dto("saldo","Long",{"saldoNome","saldoId"}))
        self.assertTrue(audit.entity_field_covered_in_dto("saldo","Long",{"saldo"}))

    def test_final_constructor_dependencies_are_parsed(self):
        result=audit.extract_fields("public class Controller { private final CommandService commands; }")
        self.assertEqual([(t,n) for t,n,a in result],[("CommandService","commands")])

    def test_a_declared_input_without_mapper_is_not_writable(self):
        self.assertEqual(mapped_input_fields("Item",{"name"},{}),set())
        mapper=info("Mapper","class Mapper implements ResourceMapper<Item,R,C,U,Long> { void apply(){entity.setName(dto.getName());} }")
        self.assertEqual(mapped_input_fields("Item",{"name","ignored"},{"Mapper":mapper}),{"name"})

    def test_readonly_projection_is_not_a_command_write(self):
        ctrl=info("Controller",'class Controller { @PostMapping("/actions/close") @WorkflowAction(id="close") public R close(){ return commands.close(); } }',[("Commands","commands","")])
        cmd=info("Commands","class Commands { public R close(){ Item e=load(); return mapper.toResponse(e); } }",[("Mapper","mapper","")])
        mapper=info("Mapper","class Mapper implements ResourceMapper<Item,R,C,U,Long> { public R toResponse(Item e){ R dto=new R();dto.setDeadline(e.getDeadline());return dto; } }")
        classes={x.name:x for x in (ctrl,cmd,mapper)}
        self.assertNotIn("deadline",command_fields(ctrl,"Item",classes))

    def test_transitive_entity_setter_is_proven_only_from_bound_handler(self):
        ctrl=info("Controller",'class Controller { @PostMapping("/actions/close") @WorkflowAction(id="close") public R close(){return commands.close();} }',[("Commands","commands","")])
        cmd=info("Commands","class Commands { public R close(){Item e=load();apply(e);return null;} private void apply(Item e){e.setDeadline(dto.deadline());} public void unrelated(){Item e=load();e.setSecret(1);} }")
        self.assertEqual(command_fields(ctrl,"Item",{"Controller":ctrl,"Commands":cmd}),{"deadline"})

    def test_other_controller_cannot_supply_write_coverage(self):
        ctrl=info("Controller","class Controller { public R get(){return null;} }")
        other=info("Other",'class Other { @WorkflowAction(id="x") @PostMapping("/actions/x") public void x(){Item e=load();e.setDeadline(1);} }')
        self.assertEqual(command_fields(ctrl,"Item",{"Controller":ctrl,"Other":other}),set())

    def test_threshold_cannot_be_weakened(self):
        result=subprocess.run([sys.executable,str(ROOT/"audit-java-resource-completeness.py"),".","--min-dto-coverage","85"],capture_output=True,text=True)
        self.assertEqual(result.returncode,2)
        self.assertIn("exactly 100%",result.stderr)

    def test_empty_project_is_not_approved(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp,"src/main/java").mkdir(parents=True)
            result=subprocess.run([sys.executable,str(ROOT/"audit-java-resource-completeness.py"),tmp,"--strict"],capture_output=True,text=True)
            self.assertEqual(result.returncode,2)

    def test_bulk_counts_effective_inherited_fields_and_real_handlers(self):
        fields=[("String","name",'@Schema(nullable=true) @BulkEditable(modes={BulkMode.UNIFORM_UPDATE,BulkMode.PER_ITEM_UPDATE},allowClear=true)')]
        source='@BulkResourceOperations class C { @Operation(operationId="eval") @PostMapping("/evaluation") public R eval(){return evaluate();} @BulkOperation(mode=BulkMode.UNIFORM_UPDATE,evaluationOperationId="eval") @PostMapping("/bulk") public R uniform(){return execute();} @BulkOperation(mode=BulkMode.PER_ITEM_UPDATE,evaluationOperationId="eval") @PostMapping("/items") public R items(){return execute();} }'
        self.assertEqual(bulk_source_summary(source,fields),(1,2,[]))

    def test_bulk_annotations_without_executable_confirmation_fail(self):
        count,ops,issues=bulk_source_summary('@BulkResourceOperations class C {}',[("String","name",'@BulkEditable')])
        self.assertEqual((count,ops),(1,0))
        self.assertEqual(len(issues),2)

    def test_bulk_clear_requires_real_schema_nullability(self):
        _,_,issues=bulk_source_summary('class C {}',[("String","name",'@BulkEditable(allowClear=true)')])
        self.assertTrue(any('schema nullability' in issue for issue in issues))
        self.assertTrue(any('@BulkResourceOperations' in issue for issue in issues))

    def test_bulk_domain_command_requires_collection_action_and_resolved_evaluation(self):
        source='@BulkResourceOperations class C { @BulkOperation(mode=BulkMode.DOMAIN_COMMAND,evaluationOperationId="absent") @WorkflowAction(scope=ActionScope.ITEM) @PostMapping("/command") public R command(){return execute();} }'
        count,ops,issues=bulk_source_summary(source,[])
        self.assertEqual((count,ops),(0,1))
        self.assertEqual(len(issues),2)

    def test_read_only_resource_requires_no_bulk(self):
        self.assertEqual(bulk_source_summary('class C {}',[]),(0,0,[]))

    def test_annotation_arrays_preserve_preceding_schema_and_ui_metadata(self):
        fields=audit.extract_fields('class D { @Schema(nullable=true) @UISchema(label="Lotação",quickViewVisible=true) @BulkEditable(modes={BulkMode.UNIFORM_UPDATE,BulkMode.PER_ITEM_UPDATE},allowClear=true) private String setor; }')
        self.assertEqual(len(fields),1)
        self.assertIn('@Schema',fields[0][2])
        self.assertIn('@UISchema',fields[0][2])
        self.assertIn('@BulkEditable',fields[0][2])

    def test_maven_dependency_changes_invalidate_operational_receipts(self):
        with tempfile.TemporaryDirectory() as tmp:
            project=Path(tmp);(project/"pom.xml").write_text("<version>first</version>")
            before=source_fingerprint(project)
            (project/"pom.xml").write_text("<version>second</version>")
            self.assertNotEqual(before,source_fingerprint(project))

    def test_resource_fact_label_sentence_is_flagged(self):
        src='@ResourceFact(key="saldo", label="Saldo disponível de vagas autorizadas no quadro de pessoal.") class C {}'
        self.assertEqual(len(resource_fact_editorial_issues(src,"C")),1)
        ok='@ResourceFact(key="saldo", label="Saldo de Vagas") class C {}'
        self.assertEqual(resource_fact_editorial_issues(ok,"C"),[])

    def test_dto_excessive_visible_table_columns_is_flagged(self):
        fields=[("String",f"f{i}",'@UISchema(label="Col")') for i in range(15)]
        self.assertEqual(len(dto_table_visibility_issues("ProjectionDTO",fields)),1)
        curated=[("String",f"f{i}",'@UISchema(label="Col"' + (',tableHidden=true' if i>=8 else '') + ')') for i in range(15)]
        self.assertEqual(dto_table_visibility_issues("ProjectionDTO",curated),[])

    def test_skeletal_entity_lookup_descriptor_is_flagged(self):
        cfg=info("OptionSourcesConfig",'class OptionSourcesConfig { void reg(){ new EntityLookupDescriptor("k","id","lbl",null,List.of(),null,null,null,null,null,LookupCapabilities.defaults()); } }')
        self.assertEqual(len(entity_lookup_descriptor_issues({"OptionSourcesConfig":cfg})),1)

    def test_rich_lookup_optional_nested_nulls_are_not_skeletal(self):
        source = 'class C { public void reg(){new EntityLookupDescriptor("k","id",List.of(),null,null,null,List.of(),Map.of(),new LookupSelectionPolicy(null,null,List.of(),List.of(),true,null,null),caps,new LookupDetailDescriptor(null,null,"drawer"),display,filtering);} }'
        self.assertEqual(entity_lookup_descriptor_issues({"C":info("C",source)}),[])
        broken=source.replace('caps,new LookupDetailDescriptor(null,null,"drawer"),display,filtering', 'caps,null,display,filtering')
        self.assertEqual(len(entity_lookup_descriptor_issues({"C":info("C",broken)})),1)

    def test_micro_visualization_getters_are_properties_not_helpers(self):
        source='class R extends Base { @MicroVisualization public Long getOcupadas(){return 2L;} @MicroVisualization public void calculate(int n){} }'
        base='class Base { @MicroVisualization public Integer getProgress(){return 1;} }'
        self.assertEqual(micro_visualization_properties("R", {"R":info("R",source),"Base":info("Base",base)}, []), {"ocupadas","progress"})

    def test_formula_is_not_a_physical_business_column(self):
        self.assertTrue(technical_or_mirrored("statusLookup", '@org.hibernate.annotations.Formula("case when ended is null then 1 else 0 end")', set()))
        self.assertFalse(technical_or_mirrored("status", '@Column(name="status")', set()))

    def test_reactive_determination_count_matches_controller_operations(self):
        ctrl='class C { @PostMapping @Operation(operationId="createItem") public R create(){return null;} @PostMapping("/det") @Operation(operationId="determineItemPreview") public P det(){return null;} }'
        cfg=info("DetCfg",'class DetCfg { ReactiveDeterminationDefinitionProvider p(){ return () -> List.of(new ReactiveDeterminationDefinition("k", List.of(new ReactiveDeterminationScope("createItem", ReactiveDeterminationFormMode.CREATE)), "determineItemPreview", ReactiveDeterminationTriggerMode.ON_CHANGE, List.of("/a"), List.of(new ReactiveDeterminationInputBinding("/a","/a")), List.of(new ReactiveDeterminationOutputBinding("/b","/b")), null)); } }')
        self.assertEqual(reactive_determination_count(ctrl, {"DetCfg":cfg}), 1)
        self.assertEqual(reactive_determination_count('class C { @PostMapping @Operation(operationId="other") public R c(){return null;} }', {"DetCfg":cfg}), 0)
        self.assertEqual(reactive_determination_issues({"DetCfg":cfg}), [])
        bad_cfg=info("BadCfg",'class BadCfg { void p(){ new ReactiveDeterminationOutputBinding("noSlash", "/ok"); } }')
        self.assertEqual(len(reactive_determination_issues({"BadCfg":bad_cfg})), 1)

if __name__=="__main__":
    unittest.main()
