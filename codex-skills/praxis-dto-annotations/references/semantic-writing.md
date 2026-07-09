# Semantic Writing For Praxis DTOs

Use this reference when writing `@Schema`, DTO class descriptions, operation text, resource
metadata, surface/action metadata, and governance metadata for a host that consumes
`praxis-metadata-starter`.

## Contents

- [Source Evidence](#source-evidence)
- [Resource And Operation Text](#resource-and-operation-text)
- [`@Schema` Rules](#schema-rules)
- [PT-BR And Terminology](#pt-br-and-terminology)
- [Governance](#governance)
- [Rejection Criteria](#rejection-criteria)

## Source Evidence

Before writing, read:

- available system documentation, functional specifications, business glossary, migration notes,
  screen documentation, user help, and legacy manuals;
- controller and operation method;
- response DTO, create DTO, update/patch DTO, action DTO, and FilterDTO;
- entity/view/projection and relationships;
- mapper/service rules and visible side effects;
- Bean Validation constraints;
- existing `@UISchema`, `@Filterable`, option-source, stats, surface, action, and governance metadata.

If a claim cannot be defended from these sources, do not write it as fact.

## Resource And Operation Text

Keep `@ApiResource(resourceKey=...)` stable and semantic. It identifies the public resource in
schema discovery, capabilities, domain catalog, config/AI surfaces, and future consumers. Do not
rename it because a controller path, Java package, or UI label changed.

Write `@Operation(summary=..., description=...)` for public operations that the host declares
explicitly. The summary should distinguish the business operation; the description should mention
real fields, dimensions, constraints, effects, and relationships.

Prefer:

```java
@Operation(
    summary = "Filtrar missões por ciclo, prioridade e ameaça",
    description = "Lista missões por status, prioridade, ameaça, local e janelas previstas ou reais para acompanhamento operacional e composição de visões de execução."
)
```

Avoid:

```java
@Operation(summary = "Filtrar registros", description = "Executa POST /filter com paginação.")
```

Use `@ResourceIntent` only for partial maintenance that remains inside the resource contract. Use
`@UiSurface` for discovery of a real UI experience over an operation. Use `@WorkflowAction` for
explicit business commands. None of these annotations defines a payload separate from
`/schemas/filtered`.

## `@Schema` Rules

Write `@Schema.description` as domain documentation for the public contract.

Do not document only the lexical meaning of the property name. Document the role that value plays in
the specific business process. The same word can mean different things in different DTOs. For
example, an `email` can be a contact channel, a login key, a notification destination, an external
identity, a holder verification attribute, or a unique registry key. The description must identify
which role is true for that resource based on documentation, rules, services, and runtime behavior.

Each property description should explain:

- what the field represents;
- how it is used in the domain;
- relevant limits, validation, lifecycle, or side effects;
- relationships with other resources or resolved display fields;
- sensitivity or governance when relevant.

Prefer:

```java
@Schema(description = "Data de início do vínculo empregatício; ancora requisitos de experiência, férias e históricos de folha.")
private LocalDate dataAdmissao;
```

Avoid:

```java
@Schema(description = "Data de admissão.")
private LocalDate dataAdmissao;
```

Prefer a business-role description over a generic word definition:

```java
@Schema(description = "E-mail principal usado como canal oficial de notificação do colaborador sobre eventos do vínculo funcional.")
private String email;
```

Avoid when the source meaning is unknown:

```java
@Schema(description = "E-mail do colaborador.")
private String email;
```

DTO-level descriptions must describe the role of the contract, not the Java class mechanics.

Prefer:

```java
@Schema(
    name = "FuncionarioDTO",
    description = "Cadastro de colaborador no domínio de RH: identificação civil, contato, remuneração, vínculo funcional e sinalizadores operacionais."
)
```

Avoid:

```java
@Schema(description = "DTO de funcionário.")
```

## PT-BR And Terminology

Use correct PT-BR with accents in public text. Technical identifiers may stay in English when they
are part of the contract (`resourceKey`, enum values, paths, JSON fields).

Prefer business language:

- `consulta`, `comando`, `cadastro`, `manutenção`, `painel`, `seleção`, `catálogo`, `opções`;
- avoid public prose centered on `endpoint`, `payload`, `lookup`, `surface`, or `CRUD` unless those
  are the actual technical contract being documented.

Avoid descriptions that add unrelated negative terms. For example, do not write "atualiza contato
sem alterar salário, cargo ou departamento" if the operation is only about contact data; those terms
pollute semantic search.

## Governance

Use `@DomainGovernance` when the field is personal, financial, legal, operationally sensitive,
credential-like, compliance-relevant, or relevant to AI policy.

Governance text must state the real reason:

```java
@DomainGovernance(
    kind = DomainGovernanceKind.PRIVACY,
    classification = DomainClassification.CONFIDENTIAL,
    dataCategory = DomainDataCategory.PERSONAL,
    complianceTags = {"LGPD"},
    aiUsage = @AiUsagePolicy(
        visibility = AiUsageMode.MASK,
        trainingUse = AiUsageMode.DENY,
        ruleAuthoring = AiUsageMode.REVIEW_REQUIRED,
        reasoningUse = AiUsageMode.REVIEW_REQUIRED
    ),
    reason = "Documento pessoal usado para identificação fiscal do colaborador."
)
```

Do not write only "dado sensível"; classify the actual data and AI usage.

## Rejection Criteria

Reject annotation text when:

- it would fit any resource;
- it explains only the dictionary meaning of a field name instead of the field's role in the
  business process;
- it only repeats the field name or `@UISchema.label`;
- it contradicts DTO, validation, mapper, service, workflow, or option-source behavior;
- it invents a rule, effect, integration, policy, permission, or metric;
- it hides a relevant side effect;
- it uses keyword stuffing or broad compliance claims without evidence;
- `@Schema.description` was generated from labels, camelCase, or a script.
