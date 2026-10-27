# Resource Baseline & First-Shot Golden Path

Use this reference when implementing concrete resources in a new or existing Praxis Java host. It provides the exact generic signatures, package imports, and full-power code templates so the first generated slice compiles immediately and unlocks CRUD, rich filters, option lookups, analytics (`/stats/*`), quick filters, and semantic discovery (`/schemas/filtered`, `/capabilities`, HATEOAS `_links`).

## Canonical Generic Signatures & Imports Cheat-Sheet

Do not guess type parameter positions; the generic order differs across Repository, Mapper, Service, and Controller:

| Contract | Package | Exact Generic Parameter Order | Critical Method Signatures |
| --- | --- | --- | --- |
| `BaseCrudRepository` | `org.praxisplatform.uischema.repository.base` | `<E, ID>` (2 params) | Inherited Spring Data JPA + specification methods |
| `ResourceMapper` | `org.praxisplatform.uischema.mapper.base` | `<E, ResponseDTO, CreateDTO, UpdateDTO, ID>` (**5 params — `E` 1st, `ID` 5th**) | `ResponseDTO toResponse(E entity)`<br>`E newEntity(CreateDTO dto)`<br>`void applyUpdate(E entity, UpdateDTO dto)` (**`entity` is 1st!** Never overwrite `id`)<br>`ID extractId(E entity)` |
| `AbstractBaseResourceService` | `org.praxisplatform.uischema.service.base` | `<E, ResponseDTO, ID, FilterDTO, CreateDTO, UpdateDTO>` (**6 params — `E` 1st, `ID` 3rd**) | `super(repository, Entity.class)`<br>`protected ResourceMapper<E, ResponseDTO, CreateDTO, UpdateDTO, ID> getResourceMapper()` |
| `AbstractResourceController` | `org.praxisplatform.uischema.controller.base` | `<ResponseDTO, ID, FilterDTO, CreateDTO, UpdateDTO>` (**5 params — NO `E`, `ID` 2nd**) | `protected BaseResourceService<ResponseDTO, ID, FilterDTO, CreateDTO, UpdateDTO> getService()`<br>`protected ID getResponseId(ResponseDTO dto)` |
| `AbstractReadOnlyResourceService` | `org.praxisplatform.uischema.service.base` | `<E, ResponseDTO, ID, FilterDTO>` (**4 params — `E` 1st, `ID` 3rd**) | `super(repository, Entity.class)`<br>`protected ResourceMapper<E, ResponseDTO, ?, ?, ID> getResourceMapper()` |
| `AbstractReadOnlyResourceController` | `org.praxisplatform.uischema.controller.base` | `<ResponseDTO, ID, FilterDTO>` (**3 params — NO `E`, `ID` 2nd**) | `protected BaseResourceQueryService<ResponseDTO, ID, FilterDTO> getService()`<br>`protected ID getResponseId(ResponseDTO dto)` |
| `VersionedCreateUpdateResourceService` | `org.praxisplatform.uischema.service.base` | `<ResponseDTO, ID, FilterDTO, CreateDTO, UpdateDTO>` (**5 params — NO `E`, `ID` 2nd**) | `protected OptionalLong getEntityResourceVersion(E entity)`<br>`ResourceRepresentationResult<ResponseDTO> update(ID id, UpdateDTO dto, ResourceVersionUpdatePrecondition<ID> precondition)` |
| `CompositeResourceId` | `org.praxisplatform.uischema.id` | Marker interface on `@Embeddable` `record`/class | Auto-serializes composite keys as `"part1:part2"` across URLs, JSON, OpenAPI (`format: "composite-id"`), Criteria, Sort, Options & Export |

### Canonical Starter Imports

```java
// Resource & Discovery Annotations
import org.praxisplatform.uischema.annotation.ApiGroup;
import org.praxisplatform.uischema.annotation.ApiResource;
import org.praxisplatform.uischema.annotation.OptionLabel;
import org.praxisplatform.uischema.annotation.QuickFilter;
import org.praxisplatform.uischema.annotation.ResourceIdentity;
import org.praxisplatform.uischema.annotation.ResourceIntent;
import org.praxisplatform.uischema.annotation.ResourceReference;
import org.praxisplatform.uischema.annotation.UiSurface;
import org.praxisplatform.uischema.annotation.WorkflowAction;

// Composite Keys, Custom Fields & Domain Facts
import org.praxisplatform.uischema.id.CompositeResourceId;
import org.praxisplatform.uischema.customfields.CustomFields;
import org.praxisplatform.uischema.customfields.CustomFieldDataType;
import org.praxisplatform.uischema.customfields.CustomFieldDefinitionProvider;
import org.praxisplatform.uischema.customfields.CustomFieldDescriptor;
import org.praxisplatform.uischema.fact.ResourceFact;
import org.praxisplatform.uischema.fact.ResourceFacts;
import org.praxisplatform.uischema.fact.ResourceFactCatalogProvider;
import org.praxisplatform.uischema.fact.ResourceFactDescriptor;

// UI Schema & Field Presentation
import org.praxisplatform.uischema.FieldControlType;
import org.praxisplatform.uischema.FieldDataType;
import org.praxisplatform.uischema.NumericFormat;
import org.praxisplatform.uischema.extension.annotation.UISchema;
import org.praxisplatform.uischema.extension.annotation.UISchemaPreset;

// Governance & AI Policy
import org.praxisplatform.uischema.annotation.AiControlledUseMode;
import org.praxisplatform.uischema.annotation.AiTrainingUseMode;
import org.praxisplatform.uischema.annotation.AiUsagePolicy;
import org.praxisplatform.uischema.annotation.AiVisibilityMode;
import org.praxisplatform.uischema.annotation.DomainClassification;
import org.praxisplatform.uischema.annotation.DomainDataCategory;
import org.praxisplatform.uischema.annotation.DomainGovernance;
import org.praxisplatform.uischema.annotation.DomainGovernanceKind;

// Dynamic Filtering
import org.praxisplatform.uischema.filter.annotation.Filterable;
import org.praxisplatform.uischema.filter.dto.GenericFilterDTO;

// Base Hierarchy, Concurrency & Option Sources
import org.praxisplatform.uischema.repository.base.BaseCrudRepository;
import org.praxisplatform.uischema.mapper.base.ResourceMapper;
import org.praxisplatform.uischema.mapper.config.CorporateMapperConfig;
import org.praxisplatform.uischema.service.base.AbstractBaseResourceService;
import org.praxisplatform.uischema.service.base.AbstractReadOnlyResourceService;
import org.praxisplatform.uischema.service.base.VersionedCreateUpdateResourceService;
import org.praxisplatform.uischema.service.base.annotation.DefaultSortColumn;
import org.praxisplatform.uischema.concurrency.ResourceRepresentationResult;
import org.praxisplatform.uischema.concurrency.ResourceVersionPreconditionException;
import org.praxisplatform.uischema.concurrency.ResourceVersionUpdatePrecondition;
import org.praxisplatform.uischema.controller.base.AbstractResourceController;
import org.praxisplatform.uischema.controller.base.AbstractReadOnlyResourceController;
import org.praxisplatform.uischema.options.OptionSourceDescriptor;
import org.praxisplatform.uischema.options.OptionSourceRegistry;
import org.praxisplatform.uischema.options.OptionSourceType;

// Analytics / Stats
import org.praxisplatform.uischema.stats.StatsFieldRegistry;
import org.praxisplatform.uischema.stats.StatsMetric;
import org.praxisplatform.uischema.stats.StatsSupportMode;
```

## 0. Complete Project Bootstrap (`pom.xml`, `application.yml` & Main Application Class)

When scaffolding a brand-new Praxis Spring Boot host project, always emit a complete, self-contained `pom.xml` (with Java 21, `-parameters` enabled on `maven-compiler-plugin`, and `annotationProcessorPaths` when Lombok/MapStruct are used), `application.yml` (configured for PostgreSQL/Neon, OpenAPI 3.0 deterministic key ordering, and strong item `ETag` secret), and `@SpringBootApplication(scanBasePackages = {..., "org.praxisplatform.uischema"})`:

### `pom.xml`

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.5.15</version>
        <relativePath/>
    </parent>

    <groupId>com.example.hr</groupId>
    <artifactId>hr-praxis-service</artifactId>
    <version>0.1.0-SNAPSHOT</version>

    <properties>
        <java.version>21</java.version>
        <praxis.core.version>8.0.0-rc.179</praxis.core.version>
        <lombok.version>1.18.32</lombok.version>
        <org.mapstruct.version>1.5.5.Final</org.mapstruct.version>
        <lombok-mapstruct-binding.version>0.2.0</lombok-mapstruct-binding.version>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>io.github.codexrodrigues</groupId>
            <artifactId>praxis-metadata-starter</artifactId>
            <version>${praxis.core.version}</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>${lombok.version}</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>org.mapstruct</groupId>
            <artifactId>mapstruct</artifactId>
            <version>${org.mapstruct.version}</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>${java.version}</source>
                    <target>${java.version}</target>
                    <parameters>true</parameters>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                            <version>${lombok.version}</version>
                        </path>
                        <path>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok-mapstruct-binding</artifactId>
                            <version>${lombok-mapstruct-binding.version}</version>
                        </path>
                        <path>
                            <groupId>org.mapstruct</groupId>
                            <artifactId>mapstruct-processor</artifactId>
                            <version>${org.mapstruct.version}</version>
                        </path>
                    </annotationProcessorPaths>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

### `src/main/resources/application.yml`

```yaml
server:
  port: ${PORT:8080}
  forward-headers-strategy: framework

spring:
  datasource:
    url: ${SPRING_DATASOURCE_URL:jdbc:postgresql://localhost:5432/appdb}
    username: ${SPRING_DATASOURCE_USERNAME:postgres}
    password: ${SPRING_DATASOURCE_PASSWORD:postgres}
    driver-class-name: org.postgresql.Driver
  jpa:
    open-in-view: false
    hibernate:
      ddl-auto: ${SPRING_JPA_HIBERNATE_DDL_AUTO:validate}
    properties:
      hibernate:
        format_sql: false
  flyway:
    enabled: ${SPRING_FLYWAY_ENABLED:false}

springdoc:
  api-docs:
    enabled: true
    version: OPENAPI_3_0
    groups:
      enabled: true
    path: /v3/api-docs
  writer-with-order-by-keys: true

praxis:
  query:
    by-ids:
      max: 200
  pagination:
    max-size: 200
  stats:
    enabled: true
    max-buckets: 20
    max-series-points: 100
  resource-version:
    etag:
      secret: ${PRAXIS_RESOURCE_VERSION_ETAG_SECRET:dev-only-change-me-32-bytes-minimum-secret}
```

### Main Application Class (`HrPraxisApplication.java`)

```java
package com.example.hr;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication(scanBasePackages = {
        "com.example.hr",
        "org.praxisplatform.uischema"
})
public class HrPraxisApplication {
    public static void main(String[] args) {
        SpringApplication.run(HrPraxisApplication.class, args);
    }
}
```

## Required Shape

- Import contracts from the resolved starter dependency. Do not assume source files are present next to the host.
- Define public paths in an `ApiPaths` class. Do not scatter path literals.
- Annotate controllers with `@ApiResource(value = ApiPaths..., resourceKey = "...")`, enriched with `title`, `description`, `icon`, `visualTone`, `identity = @ResourceIdentity(...)`, and `quickFilters = {@QuickFilter(...)}`.
- Use stable `resourceKey` values such as `human-resources.employees` or `administracao-pessoal.colaboradores`; they are public identity, not local labels.
- Use `@ApiGroup` when the group becomes part of public OpenAPI discovery.
- Use `BaseCrudRepository<E, ID>` for CRUD and query resources.
- Use `AbstractBaseResourceService<E, ResponseDTO, ID, FilterDTO, CreateDTO, UpdateDTO>` or a thin host-local subclass.
- Use `AbstractReadOnlyResourceService<E, ResponseDTO, ID, FilterDTO>` and `AbstractReadOnlyResourceController<ResponseDTO, ID, FilterDTO>` for database views, analytics projections, read models, and resources that must not publish create/update/delete.
- Use `ResourceMapper<E, ResponseDTO, CreateDTO, UpdateDTO, ID>` as the service boundary. A concrete mapper may implement the interface directly, or a thin host-local base service may adapt MapStruct methods/functions to a `ResourceMapper`.
- Prefer MapStruct for DTO/entity conversion when the host has multiple resources.
- Host-local base classes are allowed when they stay thin and pedagogical, as in the quickstart pattern: they may centralize repeated mapper wiring, stats OpenAPI examples, dataset-version defaults, or HATEOAS helpers, but they must still extend/delegate to the Praxis base controller/service and must not redefine resource semantics.
- Do not add `@RestController` by reflex. In the current starter, `@ApiResource` is meta-annotated with `@RestController` and `@RequestMapping`.

## Generation Inputs And Order

Before generating code, obtain or infer:

- base package and module package;
- entity or projection name, ID type, mutability/read-only mode, and table/view source;
- `resourcePath`, stable `resourceKey`, and `@ApiGroup`;
- DTO fields, validation constraints, relationships, option labels, sensitive fields, and domain descriptions;
- filter fields and `Filterable.FilterOperation` choices;
- stats fields (`StatsFieldRegistry`) so group-by, time-series, and distribution endpoints work out of the box;
- whether option-sources, export, surfaces, resource intents, or workflow actions are required.

Safe generation order for a new application is:
1. `ApiPaths`
2. Entity/projection (with `@OptionLabel` and `@DefaultSortColumn`)
3. `BaseCrudRepository`
4. DTOs (`ResponseDTO`, `CreateDTO`, `UpdateDTO`, `FilterDTO`)
5. `ResourceMapper`
6. `Service` (with `StatsFieldRegistry` and `getDatasetVersion()`)
7. `Controller` (with `@ApiResource` and `@ApiGroup`)
8. Optional `@UiSurface`, `@ResourceIntent`, `@WorkflowAction`, or collection export.

## Complete 1-Shot Golden Path Template (Mutable Resource)

### 1. `ApiPaths.java`

```java
package com.example.hr.constants;

public final class ApiPaths {
    private ApiPaths() {}

    public static final class HumanResources {
        public static final String EMPLOYEES = "/api/human-resources/employees";
        public static final String DEPARTMENTS = "/api/human-resources/departments";

        private HumanResources() {}
    }
}
```

### 2. Entity (`Employee.java`) with `@OptionLabel` and `@DefaultSortColumn`

```java
package com.example.hr.employee.entity;

import jakarta.persistence.*;
import org.praxisplatform.uischema.annotation.OptionLabel;
import org.praxisplatform.uischema.service.base.annotation.DefaultSortColumn;

import java.math.BigDecimal;
import java.time.LocalDate;

@Entity
@Table(name = "employees")
public class Employee {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @DefaultSortColumn(priority = 1, ascending = true)
    @Column(name = "full_name", nullable = false, length = 200)
    private String fullName;

    @Column(name = "email", nullable = false, length = 200)
    private String email;

    @Column(name = "department_name", nullable = false, length = 120)
    private String departmentName;

    @Column(name = "salary", nullable = false, precision = 15, scale = 2)
    private BigDecimal salary;

    @Column(name = "hire_date", nullable = false)
    private LocalDate hireDate;

    @Column(name = "active", nullable = false)
    private Boolean active = Boolean.TRUE;

    @OptionLabel
    public String getFullName() {
        return fullName;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public void setFullName(String fullName) { this.fullName = fullName; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getDepartmentName() { return departmentName; }
    public void setDepartmentName(String departmentName) { this.departmentName = departmentName; }
    public BigDecimal getSalary() { return salary; }
    public void setSalary(BigDecimal salary) { this.salary = salary; }
    public LocalDate getHireDate() { return hireDate; }
    public void setHireDate(LocalDate hireDate) { this.hireDate = hireDate; }
    public Boolean getActive() { return active; }
    public void setActive(Boolean active) { this.active = active; }
}
```

### 3. Repository (`EmployeeRepository.java`)

```java
package com.example.hr.employee.repository;

import com.example.hr.employee.entity.Employee;
import org.praxisplatform.uischema.repository.base.BaseCrudRepository;

public interface EmployeeRepository extends BaseCrudRepository<Employee, Long> {
}
```

### 4. The 4 Rich DTOs (`ResponseDTO`, `CreateDTO`, `UpdateDTO`, `FilterDTO`)

```java
package com.example.hr.employee.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import org.praxisplatform.uischema.FieldControlType;
import org.praxisplatform.uischema.FieldDataType;
import org.praxisplatform.uischema.NumericFormat;
import org.praxisplatform.uischema.annotation.*;
import org.praxisplatform.uischema.extension.annotation.UISchema;
import org.praxisplatform.uischema.extension.annotation.UISchemaPreset;

import java.math.BigDecimal;
import java.time.LocalDate;

@Schema(
    name = "EmployeeResponseDTO",
    description = "Visão cadastral e funcional do colaborador no domínio de RH, reunindo identificação, lotação organizacional, remuneração base, data de admissão e situação operacional."
)
@ResourceIdentity(
    keyField = "id",
    titleField = "fullName",
    subtitleField = "departmentName",
    metadataFields = {"email", "hireDate"},
    displayLabelField = "fullName"
)
public class EmployeeResponseDTO {

    @Schema(description = "Identificador único do registro do colaborador no cadastro de RH.", example = "101")
    @UISchema(
        preset = UISchemaPreset.ENTERPRISE_ID,
        label = "Código",
        type = FieldDataType.NUMBER,
        numericFormat = NumericFormat.INTEGER,
        readOnly = true,
        formHidden = true,
        group = "Identificação",
        order = 1,
        icon = "tag"
    )
    private Long id;

    @Schema(description = "Nome civil completo do colaborador utilizado em contratos, listagens operacionais e identificação funcional.", example = "Ana Beatriz Costa")
    @UISchema(
        preset = UISchemaPreset.ENTERPRISE_NAME,
        label = "Nome Completo",
        group = "Identificação",
        order = 10,
        icon = "badge",
        quickViewVisible = true,
        quickViewOrder = 10,
        helpText = "Nome civil completo conforme registro funcional."
    )
    private String fullName;

    @DomainGovernance(
        kind = DomainGovernanceKind.PRIVACY,
        classification = DomainClassification.CONFIDENTIAL,
        dataCategory = DomainDataCategory.PERSONAL,
        complianceTags = {"LGPD"},
        aiUsage = @AiUsagePolicy(
            visibility = AiVisibilityMode.MASK,
            trainingUse = AiTrainingUseMode.DENY,
            ruleAuthoring = AiControlledUseMode.REVIEW_REQUIRED,
            reasoningUse = AiControlledUseMode.ALLOW
        ),
        reason = "Canal de contato corporativo e pessoal do colaborador."
    )
    @Schema(description = "Endereço de e-mail corporativo do colaborador utilizado para comunicações oficiais e notificações de fluxo.", example = "ana.costa@empresa.com.br")
    @UISchema(
        label = "E-mail",
        type = FieldDataType.EMAIL,
        controlType = FieldControlType.EMAIL_INPUT,
        group = "Identificação",
        order = 20,
        icon = "email",
        helpText = "E-mail corporativo ativo do colaborador."
    )
    private String email;

    @Schema(description = "Unidade organizacional ou departamento em que o colaborador está alocado para fins de gestão e centro de custo.", example = "Engenharia de Plataforma")
    @UISchema(
        label = "Departamento",
        group = "Vínculo e Remuneração",
        order = 10,
        icon = "apartment",
        quickViewVisible = true,
        quickViewOrder = 20,
        helpText = "Departamento de lotação atual."
    )
    private String departmentName;

    @DomainGovernance(
        kind = DomainGovernanceKind.PRIVACY,
        classification = DomainClassification.CONFIDENTIAL,
        dataCategory = DomainDataCategory.FINANCIAL,
        complianceTags = {"LGPD", "INTERNAL_POLICY"},
        aiUsage = @AiUsagePolicy(
            visibility = AiVisibilityMode.MASK,
            trainingUse = AiTrainingUseMode.DENY,
            ruleAuthoring = AiControlledUseMode.REVIEW_REQUIRED,
            reasoningUse = AiControlledUseMode.ALLOW
        ),
        reason = "Remuneração contratual individual sujeita a sigilo salarial."
    )
    @Schema(description = "Remuneração mensal base vigente do colaborador em moeda corrente, utilizada em folha e análises de orçamento.", example = "12500.00")
    @UISchema(
        preset = UISchemaPreset.MONETARY_AMOUNT,
        label = "Salário Base",
        type = FieldDataType.NUMBER,
        controlType = FieldControlType.CURRENCY_INPUT,
        numericFormat = NumericFormat.CURRENCY,
        group = "Vínculo e Remuneração",
        order = 20,
        icon = "payments",
        helpText = "Valor bruto mensal contratado."
    )
    private BigDecimal salary;

    @Schema(description = "Data de início efetivo do vínculo do colaborador na organização, base para cálculo de tempo de casa e elegibilidades.", example = "2024-03-15")
    @UISchema(
        label = "Data de Admissão",
        type = FieldDataType.DATE,
        controlType = FieldControlType.DATE_PICKER,
        numericFormat = NumericFormat.DATE,
        mask = "dd/MM/yyyy",
        group = "Vínculo e Remuneração",
        order = 30,
        icon = "event_available",
        quickViewVisible = true,
        quickViewOrder = 30,
        helpText = "Data oficial de admissão."
    )
    private LocalDate hireDate;

    @Schema(description = "Indicador de vínculo ativo do colaborador; registros inativos permanecem disponíveis para histórico e auditoria.", example = "true")
    @UISchema(
        preset = UISchemaPreset.BOOLEAN_FLAG,
        label = "Ativo",
        type = FieldDataType.BOOLEAN,
        controlType = FieldControlType.CHECKBOX,
        group = "Situação Operacional",
        order = 10,
        icon = "toggle_on",
        quickViewVisible = true,
        quickViewOrder = 40,
        labelTrue = "Ativo",
        labelFalse = "Inativo",
        toneTrue = "success",
        toneFalse = "neutral",
        helpText = "Indica se o colaborador está em exercício ativo."
    )
    private Boolean active;

    // Getters and setters...
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getFullName() { return fullName; }
    public void setFullName(String fullName) { this.fullName = fullName; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getDepartmentName() { return departmentName; }
    public void setDepartmentName(String departmentName) { this.departmentName = departmentName; }
    public BigDecimal getSalary() { return salary; }
    public void setSalary(BigDecimal salary) { this.salary = salary; }
    public LocalDate getHireDate() { return hireDate; }
    public void setHireDate(LocalDate hireDate) { this.hireDate = hireDate; }
    public Boolean getActive() { return active; }
    public void setActive(Boolean active) { this.active = active; }
}
```

```java
package com.example.hr.employee.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.*;
import org.praxisplatform.uischema.FieldControlType;
import org.praxisplatform.uischema.FieldDataType;
import org.praxisplatform.uischema.NumericFormat;
import org.praxisplatform.uischema.extension.annotation.UISchema;
import org.praxisplatform.uischema.extension.annotation.UISchemaPreset;

import java.math.BigDecimal;
import java.time.LocalDate;

@JsonIgnoreProperties({"id"})
@Schema(
    name = "CreateEmployeeDTO",
    description = "Contrato de entrada para admissão e cadastro inicial de um novo colaborador no domínio de RH."
)
public class CreateEmployeeDTO {

    @NotBlank
    @Size(max = 200)
    @Schema(description = "Nome civil completo do colaborador para registro contratual e exibição em sistemas internos.", example = "Ana Beatriz Costa")
    @UISchema(preset = UISchemaPreset.ENTERPRISE_NAME, label = "Nome Completo", required = true, maxLength = 200, group = "Identificação", order = 10, icon = "badge", helpText = "Informe o nome civil completo.")
    private String fullName;

    @NotBlank
    @Email
    @Size(max = 200)
    @Schema(description = "Endereço de e-mail corporativo atribuído ao colaborador no processo de admissão.", example = "ana.costa@empresa.com.br")
    @UISchema(label = "E-mail", type = FieldDataType.EMAIL, controlType = FieldControlType.EMAIL_INPUT, required = true, maxLength = 200, group = "Identificação", order = 20, icon = "email", helpText = "Informe o e-mail corporativo.")
    private String email;

    @NotBlank
    @Size(max = 120)
    @Schema(description = "Departamento organizacional em que o colaborador iniciará suas atividades.", example = "Engenharia de Plataforma")
    @UISchema(label = "Departamento", required = true, maxLength = 120, group = "Vínculo e Remuneração", order = 10, icon = "apartment", helpText = "Informe o departamento de lotação inicial.")
    private String departmentName;

    @NotNull
    @DecimalMin("0.00")
    @Schema(description = "Salário mensal bruto inicial definido na proposta de contratação.", example = "12500.00")
    @UISchema(preset = UISchemaPreset.MONETARY_AMOUNT, label = "Salário Base", type = FieldDataType.NUMBER, controlType = FieldControlType.CURRENCY_INPUT, numericFormat = NumericFormat.CURRENCY, required = true, min = "0.00", group = "Vínculo e Remuneração", order = 20, icon = "payments", helpText = "Informe a remuneração base mensal.")
    private BigDecimal salary;

    @NotNull
    @Schema(description = "Data oficial de início do vínculo contratual do colaborador.", example = "2024-03-15")
    @UISchema(label = "Data de Admissão", type = FieldDataType.DATE, controlType = FieldControlType.DATE_PICKER, numericFormat = NumericFormat.DATE, mask = "dd/MM/yyyy", required = true, group = "Vínculo e Remuneração", order = 30, icon = "event_available", helpText = "Selecione a data de admissão.")
    private LocalDate hireDate;

    @NotNull
    @Schema(description = "Define se o registro já nasce ativo para operações imediatas.", example = "true")
    @UISchema(preset = UISchemaPreset.BOOLEAN_FLAG, label = "Ativo", type = FieldDataType.BOOLEAN, controlType = FieldControlType.CHECKBOX, required = true, group = "Situação Operacional", order = 10, icon = "toggle_on", helpText = "Marque para ativar o colaborador imediatamente.")
    private Boolean active = Boolean.TRUE;

    // Getters and setters...
    public String getFullName() { return fullName; }
    public void setFullName(String fullName) { this.fullName = fullName; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getDepartmentName() { return departmentName; }
    public void setDepartmentName(String departmentName) { this.departmentName = departmentName; }
    public BigDecimal getSalary() { return salary; }
    public void setSalary(BigDecimal salary) { this.salary = salary; }
    public LocalDate getHireDate() { return hireDate; }
    public void setHireDate(LocalDate hireDate) { this.hireDate = hireDate; }
    public Boolean getActive() { return active; }
    public void setActive(Boolean active) { this.active = active; }
}
```

```java
package com.example.hr.employee.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.*;
import org.praxisplatform.uischema.FieldControlType;
import org.praxisplatform.uischema.FieldDataType;
import org.praxisplatform.uischema.NumericFormat;
import org.praxisplatform.uischema.extension.annotation.UISchema;
import org.praxisplatform.uischema.extension.annotation.UISchemaPreset;

import java.math.BigDecimal;
import java.time.LocalDate;

@JsonIgnoreProperties({"id"})
@Schema(
    name = "UpdateEmployeeDTO",
    description = "Contrato de atualização cadastral e contratual de um colaborador existente, preservando a identidade da rota."
)
public class UpdateEmployeeDTO {

    @NotBlank
    @Size(max = 200)
    @Schema(description = "Nome civil completo atualizado do colaborador.", example = "Ana Beatriz Costa")
    @UISchema(preset = UISchemaPreset.ENTERPRISE_NAME, label = "Nome Completo", required = true, maxLength = 200, group = "Identificação", order = 10, icon = "badge", helpText = "Atualize o nome civil completo se necessário.")
    private String fullName;

    @NotBlank
    @Email
    @Size(max = 200)
    @Schema(description = "Endereço de e-mail corporativo atualizado do colaborador.", example = "ana.costa@empresa.com.br")
    @UISchema(label = "E-mail", type = FieldDataType.EMAIL, controlType = FieldControlType.EMAIL_INPUT, required = true, maxLength = 200, group = "Identificação", order = 20, icon = "email", helpText = "Atualize o e-mail corporativo.")
    private String email;

    @NotBlank
    @Size(max = 120)
    @Schema(description = "Departamento organizacional atual do colaborador.", example = "Engenharia de Plataforma")
    @UISchema(label = "Departamento", required = true, maxLength = 120, group = "Vínculo e Remuneração", order = 10, icon = "apartment", helpText = "Atualize o departamento de lotação.")
    private String departmentName;

    @NotNull
    @DecimalMin("0.00")
    @Schema(description = "Salário mensal base vigente após revisão ou enquadramento.", example = "13200.00")
    @UISchema(preset = UISchemaPreset.MONETARY_AMOUNT, label = "Salário Base", type = FieldDataType.NUMBER, controlType = FieldControlType.CURRENCY_INPUT, numericFormat = NumericFormat.CURRENCY, required = true, min = "0.00", group = "Vínculo e Remuneração", order = 20, icon = "payments", helpText = "Informe o salário base vigente.")
    private BigDecimal salary;

    @NotNull
    @Schema(description = "Data oficial de admissão registrada no vínculo.", example = "2024-03-15")
    @UISchema(label = "Data de Admissão", type = FieldDataType.DATE, controlType = FieldControlType.DATE_PICKER, numericFormat = NumericFormat.DATE, mask = "dd/MM/yyyy", required = true, group = "Vínculo e Remuneração", order = 30, icon = "event_available", helpText = "Data de início do vínculo.")
    private LocalDate hireDate;

    @NotNull
    @Schema(description = "Indicador de vínculo ativo do colaborador no cadastro.", example = "true")
    @UISchema(preset = UISchemaPreset.BOOLEAN_FLAG, label = "Ativo", type = FieldDataType.BOOLEAN, controlType = FieldControlType.CHECKBOX, required = true, group = "Situação Operacional", order = 10, icon = "toggle_on", helpText = "Indica se o vínculo permanece ativo.")
    private Boolean active;

    // Getters and setters...
    public String getFullName() { return fullName; }
    public void setFullName(String fullName) { this.fullName = fullName; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getDepartmentName() { return departmentName; }
    public void setDepartmentName(String departmentName) { this.departmentName = departmentName; }
    public BigDecimal getSalary() { return salary; }
    public void setSalary(BigDecimal salary) { this.salary = salary; }
    public LocalDate getHireDate() { return hireDate; }
    public void setHireDate(LocalDate hireDate) { this.hireDate = hireDate; }
    public Boolean getActive() { return active; }
    public void setActive(Boolean active) { this.active = active; }
}
```

```java
package com.example.hr.employee.dto.filter;

import io.swagger.v3.oas.annotations.media.Schema;
import org.praxisplatform.uischema.FieldControlType;
import org.praxisplatform.uischema.FieldDataType;
import org.praxisplatform.uischema.NumericFormat;
import org.praxisplatform.uischema.extension.annotation.UISchema;
import org.praxisplatform.uischema.filter.annotation.Filterable;
import org.praxisplatform.uischema.filter.dto.GenericFilterDTO;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

@Schema(
    name = "EmployeeFilterDTO",
    description = "Critérios de pesquisa avançada de colaboradores por identificação, departamento, situação cadastral, faixa salarial e janelas de admissão."
)
public class EmployeeFilterDTO implements GenericFilterDTO {

    @Schema(description = "Trecho do nome civil do colaborador para busca textual parcial.")
    @UISchema(label = "Nome Completo", controlType = FieldControlType.INPUT, order = 10, icon = "badge", helpText = "Digite parte do nome do colaborador.")
    @Filterable(operation = Filterable.FilterOperation.LIKE)
    private String fullName;

    @Schema(description = "Trecho do endereço de e-mail corporativo para localização rápida.")
    @UISchema(label = "E-mail", type = FieldDataType.EMAIL, controlType = FieldControlType.INPUT, order = 20, icon = "email", helpText = "Buscar por trecho do e-mail.")
    @Filterable(operation = Filterable.FilterOperation.LIKE)
    private String email;

    @Schema(description = "Nome ou trecho do departamento para filtrar colaboradores por lotação organizacional.")
    @UISchema(label = "Departamento", controlType = FieldControlType.INPUT, order = 30, icon = "apartment", helpText = "Filtrar pelo nome do departamento.")
    @Filterable(operation = Filterable.FilterOperation.LIKE)
    private String departmentName;

    @Schema(description = "Situação operacional do vínculo para restringir a listagem a ativos ou inativos.")
    @UISchema(label = "Ativo", type = FieldDataType.BOOLEAN, controlType = FieldControlType.CHECKBOX, order = 40, icon = "toggle_on", helpText = "Filtrar apenas colaboradores ativos ou inativos.")
    @Filterable(operation = Filterable.FilterOperation.EQUAL)
    private Boolean active;

    @Schema(description = "Faixa de remuneração base mensal (mínimo e máximo) para recortes orçamentários.")
    @UISchema(label = "Faixa Salarial", type = FieldDataType.NUMBER, controlType = FieldControlType.PRICE_RANGE, numericFormat = NumericFormat.CURRENCY, numericStep = "0.01", order = 50, icon = "payments", helpText = "Informe o salário mínimo e máximo.")
    @Filterable(operation = Filterable.FilterOperation.BETWEEN, relation = "salary")
    private List<BigDecimal> salaryBetween;

    @Schema(description = "Intervalo de datas de admissão para análise de coortes de contratação.")
    @UISchema(label = "Período de Admissão", type = FieldDataType.DATE, controlType = FieldControlType.DATE_RANGE, order = 60, icon = "event", helpText = "Selecione a data inicial e final de admissão.")
    @Filterable(operation = Filterable.FilterOperation.BETWEEN, relation = "hireDate")
    private List<LocalDate> hireDateRange;

    @Schema(description = "Quantidade de dias recentes para localizar colaboradores admitidos na última janela móvel.")
    @UISchema(label = "Admitidos nos últimos (dias)", type = FieldDataType.NUMBER, controlType = FieldControlType.INPUT, order = 70, icon = "history", helpText = "Ex.: 30 para admitidos nos últimos 30 dias.")
    @Filterable(operation = Filterable.FilterOperation.IN_LAST_DAYS, relation = "hireDate")
    private Integer hireDateLastDays;

    // Getters and setters...
    public String getFullName() { return fullName; }
    public void setFullName(String fullName) { this.fullName = fullName; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getDepartmentName() { return departmentName; }
    public void setDepartmentName(String departmentName) { this.departmentName = departmentName; }
    public Boolean getActive() { return active; }
    public void setActive(Boolean active) { this.active = active; }
    public List<BigDecimal> getSalaryBetween() { return salaryBetween; }
    public void setSalaryBetween(List<BigDecimal> salaryBetween) { this.salaryBetween = salaryBetween; }
    public List<LocalDate> getHireDateRange() { return hireDateRange; }
    public void setHireDateRange(List<LocalDate> hireDateRange) { this.hireDateRange = hireDateRange; }
    public Integer getHireDateLastDays() { return hireDateLastDays; }
    public void setHireDateLastDays(Integer hireDateLastDays) { this.hireDateLastDays = hireDateLastDays; }
}
```

### 5. `ResourceMapper` (`EmployeeMapper.java` — Preserving Route Identity on Update)

```java
package com.example.hr.employee.mapper;

import com.example.hr.employee.dto.CreateEmployeeDTO;
import com.example.hr.employee.dto.EmployeeResponseDTO;
import com.example.hr.employee.dto.UpdateEmployeeDTO;
import com.example.hr.employee.entity.Employee;
import org.praxisplatform.uischema.mapper.base.ResourceMapper;
import org.springframework.stereotype.Component;

@Component
public class EmployeeMapper implements ResourceMapper<
        Employee,
        EmployeeResponseDTO,
        CreateEmployeeDTO,
        UpdateEmployeeDTO,
        Long> {

    @Override
    public EmployeeResponseDTO toResponse(Employee entity) {
        EmployeeResponseDTO dto = new EmployeeResponseDTO();
        dto.setId(entity.getId());
        dto.setFullName(entity.getFullName());
        dto.setEmail(entity.getEmail());
        dto.setDepartmentName(entity.getDepartmentName());
        dto.setSalary(entity.getSalary());
        dto.setHireDate(entity.getHireDate());
        dto.setActive(entity.getActive());
        return dto;
    }

    @Override
    public Employee newEntity(CreateEmployeeDTO dto) {
        Employee entity = new Employee();
        entity.setFullName(dto.getFullName());
        entity.setEmail(dto.getEmail());
        entity.setDepartmentName(dto.getDepartmentName());
        entity.setSalary(dto.getSalary());
        entity.setHireDate(dto.getHireDate());
        entity.setActive(dto.getActive() != null ? dto.getActive() : Boolean.TRUE);
        return entity;
    }

    @Override
    public void applyUpdate(Employee entity, UpdateEmployeeDTO dto) {
        // Never overwrite entity.setId(...) or route-owned technical keys!
        entity.setFullName(dto.getFullName());
        entity.setEmail(dto.getEmail());
        entity.setDepartmentName(dto.getDepartmentName());
        entity.setSalary(dto.getSalary());
        entity.setHireDate(dto.getHireDate());
        entity.setActive(dto.getActive());
    }

    @Override
    public Long extractId(Employee entity) {
        return entity.getId();
    }
}
```

### 6. Service (`EmployeeService.java` — With `StatsFieldRegistry` & `getDatasetVersion()`)

```java
package com.example.hr.employee.service;

import com.example.hr.employee.dto.CreateEmployeeDTO;
import com.example.hr.employee.dto.EmployeeResponseDTO;
import com.example.hr.employee.dto.UpdateEmployeeDTO;
import com.example.hr.employee.dto.filter.EmployeeFilterDTO;
import com.example.hr.employee.entity.Employee;
import com.example.hr.employee.mapper.EmployeeMapper;
import com.example.hr.employee.repository.EmployeeRepository;
import org.praxisplatform.uischema.mapper.base.ResourceMapper;
import org.praxisplatform.uischema.service.base.AbstractBaseResourceService;
import org.praxisplatform.uischema.stats.StatsFieldRegistry;
import org.praxisplatform.uischema.stats.StatsMetric;
import org.praxisplatform.uischema.stats.StatsSupportMode;
import org.springframework.stereotype.Service;

import java.util.Optional;
import java.util.Set;

@Service
public class EmployeeService extends AbstractBaseResourceService<
        Employee,
        EmployeeResponseDTO,
        Long,
        EmployeeFilterDTO,
        CreateEmployeeDTO,
        UpdateEmployeeDTO> {

    private static final StatsFieldRegistry STATS_FIELDS = StatsFieldRegistry.builder()
            .categoricalGroupByBucket("active", "active")
            .groupByBucket("departmentName", "departmentName", Set.of(StatsMetric.COUNT))
            .temporalTimeSeriesField("hireDate", "hireDate")
            .numericHistogramMeasureField("salary", "salary")
            .build();

    private final EmployeeMapper mapper;

    public EmployeeService(EmployeeRepository repository, EmployeeMapper mapper) {
        super(repository, Employee.class);
        this.mapper = mapper;
    }

    @Override
    protected ResourceMapper<Employee, EmployeeResponseDTO, CreateEmployeeDTO, UpdateEmployeeDTO, Long> getResourceMapper() {
        return mapper;
    }

    @Override
    public Optional<String> getDatasetVersion() {
        return Optional.of("Employee:" + getRepository().count());
    }

    @Override
    public StatsFieldRegistry getStatsFieldRegistry() {
        return STATS_FIELDS;
    }

    @Override
    public StatsSupportMode getGroupByStatsSupportMode() {
        return StatsSupportMode.AUTO;
    }

    @Override
    public StatsSupportMode getTimeSeriesStatsSupportMode() {
        return StatsSupportMode.AUTO;
    }

    @Override
    public StatsSupportMode getDistributionStatsSupportMode() {
        return StatsSupportMode.AUTO;
    }

    @Override
    public StatsSupportMode getComparisonStatsSupportMode() {
        return StatsSupportMode.AUTO;
    }
}
```

### 7. Controller (`EmployeeController.java` — With `@ApiResource`, `@ResourceIdentity`, `@QuickFilter`, `@ApiGroup`)

```java
package com.example.hr.employee.controller;

import com.example.hr.constants.ApiPaths;
import com.example.hr.employee.dto.CreateEmployeeDTO;
import com.example.hr.employee.dto.EmployeeResponseDTO;
import com.example.hr.employee.dto.UpdateEmployeeDTO;
import com.example.hr.employee.dto.filter.EmployeeFilterDTO;
import com.example.hr.employee.service.EmployeeService;
import org.praxisplatform.uischema.annotation.ApiGroup;
import org.praxisplatform.uischema.annotation.ApiResource;
import org.praxisplatform.uischema.annotation.QuickFilter;
import org.praxisplatform.uischema.annotation.ResourceIdentity;
import org.praxisplatform.uischema.controller.base.AbstractResourceController;

@ApiResource(
    value = ApiPaths.HumanResources.EMPLOYEES,
    resourceKey = "human-resources.employees",
    title = "Colaboradores",
    description = "Gestão cadastral, lotação organizacional, remuneração e ciclo de vida funcional de colaboradores.",
    icon = "groups",
    visualTone = "human-resources",
    identity = @ResourceIdentity(
        keyField = "id",
        titleField = "fullName",
        subtitleField = "departmentName",
        metadataFields = {"email", "hireDate"},
        displayLabelField = "fullName"
    ),
    quickFilters = {
        @QuickFilter(id = "active", label = "Ativos", filter = "active=true", icon = "check_circle"),
        @QuickFilter(id = "inactive", label = "Inativos", filter = "active=false", icon = "remove_circle_outline")
    }
)
@ApiGroup(
    value = "human-resources",
    title = "Pessoas e Recursos Humanos",
    description = "Quadros funcionais, estrutura organizacional, folha e indicadores de pessoal.",
    icon = "diversity_3",
    visualTone = "people"
)
public class EmployeeController extends AbstractResourceController<
        EmployeeResponseDTO,
        Long,
        EmployeeFilterDTO,
        CreateEmployeeDTO,
        UpdateEmployeeDTO> {

    private final EmployeeService service;

    public EmployeeController(EmployeeService service) {
        this.service = service;
    }

    @Override
    protected EmployeeService getService() {
        return service;
    }

    @Override
    protected Long getResponseId(EmployeeResponseDTO dto) {
        return dto.getId();
    }
}
```

### 8. Read-Only Variant (`AbstractReadOnlyResourceService` + `AbstractReadOnlyResourceController`)

When a resource is a database view, analytical projection, or query-only model, omit `CreateDTO` and `UpdateDTO`:

```java
@Service
public class PayrollViewService extends AbstractReadOnlyResourceService<
        PayrollView,
        PayrollViewResponseDTO,
        Long,
        PayrollViewFilterDTO> {

    private final PayrollViewMapper mapper;

    public PayrollViewService(PayrollViewRepository repository, PayrollViewMapper mapper) {
        super(repository, PayrollView.class);
        this.mapper = mapper;
    }

    @Override
    protected ResourceMapper<PayrollView, PayrollViewResponseDTO, ?, ?, Long> getResourceMapper() {
        return mapper;
    }
}

@ApiResource(
    value = ApiPaths.HumanResources.PAYROLL_VIEW,
    resourceKey = "human-resources.payroll-view",
    title = "Visão Analítica de Folha",
    description = "Projeção consolidada de competências, proventos, descontos e líquido por colaborador.",
    icon = "analytics"
)
@ApiGroup("human-resources")
public class PayrollViewController extends AbstractReadOnlyResourceController<
        PayrollViewResponseDTO,
        Long,
        PayrollViewFilterDTO> {

    private final PayrollViewService service;

    public PayrollViewController(PayrollViewService service) {
        this.service = service;
    }

    @Override
    protected PayrollViewService getService() {
        return service;
    }

    @Override
    protected Long getResponseId(PayrollViewResponseDTO dto) {
        return dto.getId();
    }
}
```

### 9. Composite Primary Key Variant (`@EmbeddedId` + `CompositeResourceId`)

When a resource has an **immutable** composite business key (e.g., `VinculoId(Long numfunc, Integer numvinc)` or `DependenteId(Long numfunc, Integer numdep)`), declare an `@Embeddable` record implementing `CompositeResourceId` and use it directly as `ID` across entity, repository, DTO, mapper, service, and controller:

```java
@Embeddable
public record VinculoId(
        @Column(name = "numfunc", nullable = false) Long numfunc,
        @Column(name = "numvinc", nullable = false) Integer numvinc
) implements CompositeResourceId {
}
```

Key corporate modeling and UX rules for composite primary keys:
- **Wire & OpenAPI:** `praxis-metadata-starter` automatically serializes/deserializes `VinculoId` as a canonical wire string (`"1001:1"`) in `@PathVariable`, `ids`, `includeIds`, `OptionDTO<VinculoId>`, `RESOURCE_ENTITY` option sources, tabular exports (CSV/Excel/JSON), and `/schemas/filtered` (`type: "string"`, `format: "composite-id"`, `x-ui.compositeIdComponents: ["numfunc", "numvinc"]`, `x-ui.compositeIdSeparator: ":"`).
- **Sorting & Criteria:** Sorting by `sort=id,desc` or `@DefaultSortColumn` on `@EmbeddedId` automatically expands to component orders (`id.numfunc DESC, id.numvinc DESC`), and `@Filterable(relation = "id.numfunc")` / `@Filterable(relation = "vinculo.id")` navigate via `.get(...)` without invalid `LEFT JOIN`s.
- **Value Objects (`@Embedded`) vs. Composite Keys (`@EmbeddedId`):** Ordinary `@Embeddable` classes used with `@Embedded` (value objects) do **not** implement `CompositeResourceId` and remain structured JSON objects in DTOs/OpenAPI while still navigating via `.get(part)` in JPA Criteria.
- **DTO & UX Contract:**
  - `ResponseDTO`: expose `VinculoId id` (`format: "composite-id"`, `formHidden = true`, `readOnly = true`) **and** individual business columns (`Long numfunc`, `Integer numvinc`) for human-readable table columns.
  - `CreateDTO`: expose separate editable business fields (`@NotNull Long numfunc`, `@NotNull Integer numvinc`) and construct `new VinculoId(dto.getNumfunc(), dto.getNumvinc())` in `ResourceMapper.newEntity(dto)`.
  - `UpdateDTO`: omit primary key components (or mark them `readOnly = true`) and **never** mutate `entity.setId(...)` in `applyUpdate`.
  - If the legacy table's natural key includes **mutable** attributes edited in `PUT /{id}` (e.g., `FREQUENCIAS` where `dtini` and `codfreq` are editable), use an immutable surrogate PK (`Long id` / `pontlei`) + `UNIQUE` constraint on the natural columns.

### 10. Optimistic Concurrency Variant (`@Version` + `VersionedCreateUpdateResourceService`)

When an entity has a `@Version` column (e.g., `private Long version = 0L;`) and `praxis.resource-version.etag.secret` is configured in `application.yml`, implement `VersionedCreateUpdateResourceService<ResponseDTO, ID, FilterDTO, CreateDTO, UpdateDTO>` on the service so that `GET /{id}` emits a signed resource version `ETag` and `PUT /{id}` enforces `If-Match` preconditions before mutating the managed entity:

```java
@Service
public class EmployeeService extends AbstractBaseResourceService<
        Employee,
        EmployeeResponseDTO,
        Long,
        EmployeeFilterDTO,
        CreateEmployeeDTO,
        UpdateEmployeeDTO>
        implements VersionedCreateUpdateResourceService<
                EmployeeResponseDTO,
                Long,
                EmployeeFilterDTO,
                CreateEmployeeDTO,
                UpdateEmployeeDTO> {

    @PersistenceContext
    private EntityManager entityManager;

    private final EmployeeMapper mapper;

    public EmployeeService(EmployeeRepository repository, EmployeeMapper mapper) {
        super(repository, Employee.class);
        this.mapper = mapper;
    }

    @Override
    protected ResourceMapper<Employee, EmployeeResponseDTO, CreateEmployeeDTO, UpdateEmployeeDTO, Long> getResourceMapper() {
        return mapper;
    }

    @Override
    protected OptionalLong getEntityResourceVersion(Employee entity) {
        return entity != null && entity.getVersion() != null
                ? OptionalLong.of(entity.getVersion())
                : OptionalLong.empty();
    }

    @Override
    @Transactional
    public ResourceRepresentationResult<EmployeeResponseDTO> update(
            Long id,
            UpdateEmployeeDTO dto,
            ResourceVersionUpdatePrecondition<Long> precondition) {
        if (precondition == null) {
            throw ResourceVersionPreconditionException.required();
        }
        Set<String> readOnlyKeys = validateCustomFields(dto, "request");
        Employee entity = findEntityById(id);
        OptionalLong currentVersion = getEntityResourceVersion(entity);
        if (currentVersion.isEmpty()) {
            throw ResourceVersionPreconditionException.missingState();
        }
        precondition.requireMatch(id, currentVersion.getAsLong());
        beforeUpdate(id, entity, dto);
        var readOnlyValues = org.praxisplatform.uischema.customfields.CustomFieldSupport.snapshotReadOnlyValues(entity, readOnlyKeys);
        mapper.applyUpdate(entity, dto);
        org.praxisplatform.uischema.customfields.CustomFieldSupport.restoreReadOnlyValues(entity, readOnlyKeys, readOnlyValues);
        Employee saved = getRepository().save(entity);
        afterUpdate(id, saved, dto);
        entityManager.flush();
        return toResourceRepresentation(saved);
    }
}
```

### 11. Governed Relationships (`@ManyToOne` / `@JoinColumns`, `@ResourceReference` & `OptionSourceRegistry`) and `@Embedded` Value Objects

#### A. Foreign Keys + Display Pairing in DTOs & `OptionSourceRegistry`
Never expose a raw foreign key in a table without its human-readable display field, and never expose a `SELECT` / `ENTITY_LOOKUP` control without a real options endpoint or governed `OptionSourceDescriptor`:

```java
// 1. In ResponseDTO: pair the FK ID (hidden in table, visible in form) with the resolved label (visible in table, hidden in form)
@Schema(description = "Identificador do cargo ocupado pelo colaborador no quadro de pessoal.", example = "10")
@UISchema(
    label = "Cargo",
    type = FieldDataType.NUMBER,
    controlType = FieldControlType.SELECT,
    group = "Lotação e Enquadramento",
    order = 10,
    tableHidden = true,
    valueField = "id",
    displayField = "label",
    endpoint = ApiPaths.HumanResources.POSITIONS
)
private Long positionId;

@Schema(description = "Nome oficial do cargo para leitura direta em listagens, cabeçalhos e exportações.", example = "Analista de Sistemas")
@UISchema(
    label = "Cargo",
    type = FieldDataType.TEXT,
    group = "Lotação e Enquadramento",
    order = 11,
    readOnly = true,
    formHidden = true
)
@ResourceReference(
    resourceKey = "human-resources.positions",
    resourcePath = ApiPaths.HumanResources.POSITIONS,
    idField = "positionId"
)
private String positionName;
```

When a foreign key uses `FieldControlType.ENTITY_LOOKUP` (or cross-field `dependsOn` / composite keys like `VinculoId`), register an `OptionSourceDescriptor` bean in an `@Configuration` class (`OptionSourceRegistry.Builder.add` takes `(Class<?> resourceClass, OptionSourceDescriptor descriptor)`):

```java
@Configuration
public class HrOptionSourcesConfig {

    @Bean
    public OptionSourceRegistry hrOptionSourceRegistry() {
        return OptionSourceRegistry.builder()
            .add(Vinculo.class, new OptionSourceDescriptor(
                "vinculoLookup",
                OptionSourceType.RESOURCE_ENTITY,
                ApiPaths.HumanResources.VINCULOS,
                "vinculo",
                "vinculo",
                "matricula",
                "id",
                List.of("empresaId"),
                Map.of("empresaId", "empresaId"), // dependent filter mapping
                OptionSourcePolicy.defaults()
            ))
            .build();
    }
}
```

#### B. `@Embedded` Value Objects (Without `CompositeResourceId`)
When multiple tables share reusable column groups (such as audit metadata, legal act snapshots, or address blocks), model them as `@Embeddable` classes annotated with `@Embedded` on the entity. Because they are **not** primary keys, they **must not** implement `CompositeResourceId`:

```java
@Embeddable
public class SnapshotAtoLegal {
    @Column(name = "numero_ato", length = 40)
    private String numeroAto;

    @Column(name = "tipo_ato", length = 30)
    private String tipoAto;

    @Column(name = "data_publicacao_ato")
    private LocalDate dataPublicacaoAto;
    // getters/setters...
}
```
In JPA Criteria (`@Filterable(relation = "atoLegal.numeroAto")`), `praxis-metadata-starter` automatically navigates `@Embedded` paths via `.get("atoLegal").get("numeroAto")` without generating invalid SQL joins.

### 12. Tenant Schema Extensibility (`@CustomFields` + `CustomFieldDefinitionProvider`) & Domain Fact Catalog (`@ResourceFact`)

#### A. JSONB `@CustomFields` in Entity, DTOs, and `CustomFieldDefinitionProvider`
When a resource supports tenant-specific dynamic fields stored in a PostgreSQL `JSONB` column (`custom_fields`) and governed by a metadata catalog table (`custom_field_definitions`):

1. **Entity (`@JdbcTypeCode(SqlTypes.JSON)`):**
```java
@JdbcTypeCode(SqlTypes.JSON)
@Column(name = "custom_fields", columnDefinition = "jsonb", nullable = false)
private Map<String, Object> customFields = new LinkedHashMap<>();
```

2. **`ResponseDTO`, `CreateDTO`, `UpdateDTO`, and `FilterDTO` (`@CustomFields`):**
```java
@Schema(description = "Atributos dinâmicos específicos do órgão/tenant governados pelo catálogo de campos customizados.")
@CustomFields(resourceKey = "human-resources.employees")
private Map<String, Object> customFields = new LinkedHashMap<>();
```
*(Keep `customFields` as an explicit nested map on the wire — `{"fullName": "Ana", "customFields": {"numero_calcado": 42}}`; never add `@JsonAnyGetter`/`@JsonAnySetter` to the root DTO).*

3. **Host `CustomFieldDefinitionProvider` Bean:**
Register a `@Component` implementing `CustomFieldDefinitionProvider` (and optionally `ResourceTenantContextResolver` when overriding the default `X-Tenant` / `X-Tenant-ID` header resolution) that queries your `custom_field_definitions` catalog table and returns `List<CustomFieldDescriptor>`:
```java
public record CustomFieldDescriptor(
    String key, String label, String description, CustomFieldDataType dataType,
    FieldControlType controlType, String group, int order, boolean required, boolean readOnly,
    boolean filterable, boolean sortable, boolean exportable, Object defaultValue,
    BigDecimal minimum, BigDecimal maximum, Integer minLength, Integer maxLength,
    String pattern, String patternMessage, String requiredMessage, List<String> enumValues,
    List<Map<String, Object>> options, OptionSourceDescriptor optionSource,
    Filterable.FilterOperation filterOperation, Map<String, Object> governance
)
```
*(Note: `key` must match `[a-zA-Z][a-zA-Z0-9_]{0,63}` and must not be any reserved JS object key: `constructor`, `prototype`, `hasOwnProperty`, `isPrototypeOf`, `propertyIsEnumerable`, `toLocaleString`, `toString`, `valueOf`. Return all active tenant definitions for the resource, including `readOnly` ones: `CustomFieldSchemaEnricher` automatically excludes `readOnly` fields from write `request` schemas while keeping them in `response` and eligible `filter` projections, and resolves `FieldControlType.AUTO` into concrete controls).*

The starter automatically:
- projects active tenant fields into `/schemas/filtered` under `properties.customFields` (`x-ui.customFieldsContainer: true`) and `properties.customFields.properties.<key>` (`x-ui.customField: true`, `x-ui.customFieldKey: "<key>"`, `x-ui.customFieldScope: "tenant"`);
- validates incoming `CreateDTO` / `UpdateDTO` values against the tenant's `CustomFieldDescriptor` constraints before `beforeCreate` / `beforeUpdate` and preserves `readOnly` values across updates;
- translates `filterDTO.customFields` entries into native PostgreSQL `jsonb_extract_path_text` Criteria predicates on `/filter`, `/filter/cursor`, and `/export`;
- resolves `"customFields.<key>"` dot-paths during tabular collection export (`CollectionExportValueResolver.reflective()`).

#### B. Declarative Domain Facts (`@ResourceFact` & `ResourceFactCatalogProvider`)
To publish business facts and derived domain indicators (e.g., `tempoServicoDias`, `elegivelAbonoPermanencia`, `possuiFeriasVencidas`) into `/schemas/domain` for AI/RAG discovery and rule authoring without hardcoding rules in the starter:

```java
@ResourceFact(
    key = "tempoServicoDias",
    resourceKey = "human-resources.employees",
    label = "Tempo de Serviço em Dias",
    description = "Quantidade total de dias de efetivo exercício apurada a partir da data de admissão até a data de referência.",
    dataType = "integer",
    unit = "days",
    deterministic = true,
    sourceKind = "computed"
)
@ApiResource(
    value = ApiPaths.HumanResources.EMPLOYEES,
    resourceKey = "human-resources.employees",
    title = "Colaboradores"
)
public class EmployeeController extends AbstractResourceController<...> { ... }
```
For dynamic or database-catalogued facts, register a `@Component` implementing `ResourceFactCatalogProvider`.

## Praxis Metadata Feature Coverage

For each resource, decide explicitly which Praxis metadata features are in scope:

| Feature | Host responsibility |
| --- | --- |
| OpenAPI and `x-ui` | Add deliberate `@Schema`, `@UISchema`, `@Filterable`, `@ApiResource`, and `@ApiGroup`. |
| `/schemas/filtered` | Ensure request/response DTOs are discoverable from the generated OpenAPI operation. |
| `/filter` | Implement a `GenericFilterDTO` with valid `@Filterable` operations and verify pageable SQL against the target database. |
| `/options/filter` and `/options/by-ids` | Ensure the entity has a stable id and option label, commonly with `@OptionLabel`; use `praxis-resource-entity-lookup-backend` for governed cross-resource lookups. |
| `/filter/cursor` | The starter provides baseline cursor behavior; validate sort stability and generated SQL. Override only for keyset, dialect, performance, or domain-specific behavior. |
| `/locate` | Override `locate` in the service when the UI needs position restoration. |
| `/stats/*` | Override stats support modes and publish `StatsFieldRegistry`; validate payload shape and SQL. |
| `/export` | Publish only when the service implements collection export support, capability, executor, field allowlist, limits, and truncation/audit metadata. |
| `/capabilities` | Treat as advertised capability snapshot; still execute the endpoint it advertises. |
| `/surfaces` and `/actions` | Use starter defaults only when they match the real UX contract; otherwise register/implement the required domain semantics deliberately. |
| `/schemas/domain` | Derived semantic/domain vocabulary and AI-operable catalog. Improve real DTO, operation, surface, action, `@ResourceFact`, and governance annotations; do not treat it as a structural schema source. |
| Composite PK (`@EmbeddedId`) | Implement `CompositeResourceId` on immutable `@Embeddable` PK records/classes; do **not** implement it on ordinary `@Embedded` value objects. |
| Optimistic concurrency (`ETag` / `If-Match`) | Configure `praxis.resource-version.etag.secret`, add `@Version` on the entity, and implement `VersionedCreateUpdateResourceService` (`getEntityResourceVersion` + 3-arg `update`). |
| Tenant JSONB extensibility (`@CustomFields`) | Map `custom_fields` JSONB with `@JdbcTypeCode(SqlTypes.JSON)`, annotate `Map<String, Object> customFields` with `@CustomFields(resourceKey = ...)` on DTOs/FilterDTO, and register a `CustomFieldDefinitionProvider` bean. |
| Domain Facts (`@ResourceFact`) | Annotate controllers/services with `@ResourceFact` or register `ResourceFactCatalogProvider` to publish domain indicators in `/schemas/domain`. |
| `/api/praxis/config/**` | Out of scope unless `praxis-config-starter` is intentionally included and wired. |

## DTO Rules

- Response DTOs describe the public resource state.
- Create DTOs should exclude server-owned identifiers, commonly with `@JsonIgnoreProperties({"id"})`.
- Update DTOs should express editable fields for an existing resource.
- Read-only resources should not generate create/update DTOs unless there is a real write operation elsewhere; do not expose mutable endpoints for views/projections just to satisfy a generic CRUD template.
- Filter DTOs implement `GenericFilterDTO` and use `@Filterable` on filterable fields.
- `@Schema(description=...)` must be written manually with domain semantics.
- `@UISchema` can carry labels, control hints, grouping, ordering, max length, and help text, but it is not a substitute for domain documentation.
- When using `FieldControlType` or `Filterable.FilterOperation`, verify enum values against the resolved starter jar or official docs for the target version. Common valid names include `DATE_PICKER` and `EQUAL`; do not guess aliases such as `DATEPICKER` or `EQUALS`.
- For control types expected to render in the official Angular runtime, verify runtime support with the appropriate Praxis UI/dynamic-fields guidance when there is any doubt. Java enum presence alone is not proof of frontend renderability.

## Filter Rules

- Model filters through the canonical Praxis mechanism first: `FilterDTO implements GenericFilterDTO` plus one `@Filterable(operation = Filterable.FilterOperation.<OP>)` per filterable field.
- Do not create host-local filter DSLs, ad hoc query parameters, custom request payload shapes, manual JPA `Specification` builders, or controller-specific predicate logic when the requirement fits a built-in `FilterOperation`.
- Treat `Filterable.FilterOperation` as the operation vocabulary. The metadata starter currently provides 26 built-in operations: `EQUAL`, `NOT_EQUAL`, `LIKE`, `NOT_LIKE`, `STARTS_WITH`, `ENDS_WITH`, `GREATER_THAN`, `GREATER_OR_EQUAL`, `LESS_THAN`, `LESS_OR_EQUAL`, `IN`, `NOT_IN`, `BETWEEN`, `IS_NULL`, `IS_NOT_NULL`, `BETWEEN_EXCLUSIVE`, `NOT_BETWEEN`, `OUTSIDE_RANGE`, `ON_DATE`, `IN_LAST_DAYS`, `IN_NEXT_DAYS`, `SIZE_EQ`, `SIZE_GT`, `SIZE_LT`, `IS_TRUE`, and `IS_FALSE`.
- Use `relation = "entity.path"` when the DTO field is an operational alias or targets a nested entity property, for example `statusIn` with `IN` and `relation = "status"`, or `departamentoNome` with `LIKE` and `relation = "departamento.nome"`.
- Use the canonical payload shapes expected by the starter: lists for `IN`/`NOT_IN`, range lists or supported range objects for `BETWEEN`-family operations, `Boolean.TRUE` activation for null checks, and `Integer` day counts for relative date operations.
- Add custom filtering only after proving the needed predicate cannot be expressed with the starter operation vocabulary. Keep such exceptions inside the service/repository boundary, document the reason, and avoid changing the public `/filter` contract shape unless the starter contract itself is being evolved.

## Controller Rules

Expose the inherited endpoints deliberately. For a minimal scaffold, a controller can inherit most behavior from `AbstractResourceController` and override only:

- `getService()`
- `getResponseId(ResponseDTO dto)`

Add explicit endpoint methods only when the host needs richer public OpenAPI documentation or domain-specific behavior over inherited routes. When adding them, write deliberate `@Operation` summaries/descriptions and keep paths aligned with starter conventions such as `/filter`, `/filter/cursor`, `/locate`, `/options/filter`, `/options/by-ids`, item detail, collection capabilities, and item capabilities.

For read-only resources, use the read-only controller baseline and do not publish write endpoints. The expected public surface should still include structural discovery, filter, options when supported, baseline cursor when validated, locate when implemented, stats when registered, and capabilities.

`@ResourceIntent`, `@UiSurface`, and `@WorkflowAction` must annotate real HTTP operations:

- Use `@ResourceIntent` for partial maintenance that remains inside the resource contract, such as `PATCH /{id}/profile`.
- Use `@UiSurface` for semantic discovery of an experience over a real operation; it does not define a separate payload or schema.
- Use `@WorkflowAction` only for explicit business commands, not for ordinary CRUD or partial resource maintenance.
- For item-level read/projection surfaces, set and validate `responseCardinality` against the real response shape, especially when an item endpoint returns a related collection.
- If `allowedStates`, `requiredAuthorities`, or contextual availability depend on real item state, provide a `ResourceStateSnapshotProvider`, `ActionAvailabilityRule`, or `SurfaceAvailabilityRule`; otherwise state that availability is static and validate the resulting `availability` decision in item surfaces/actions/capabilities.
- Keep `/schemas/filtered` as the structural source for request/response schemas. `/schemas/surfaces`, `/schemas/actions`, `/schemas/domain`, and capabilities are discovery or aggregate surfaces.

## Service Rules

- Implement resource services as Praxis services first, not as generic Spring services. The normal shape is a concrete class extending `AbstractBaseResourceService<E, ResponseDTO, ID, FilterDTO, CreateDTO, UpdateDTO>` or a thin host-local abstraction that still delegates to the Praxis base service.
- Keep the controller thin and let the base service handle standard list/detail/create/update/delete/filter/options behavior through `BaseCrudRepository`, `ResourceMapper`, and the typed DTO set.
- Do not reimplement ordinary CRUD, pageable filter, options id/label, schema metadata, or capability behavior in the service when the base resource service already provides it.
- Keep domain update semantics explicit in `applyUpdate`; do not blindly replace persistent entities.
- Keep mapper semantics at the `ResourceMapper` boundary. Avoid hand-mapping DTOs throughout service methods except for small, explicit domain exceptions.
- Override `getIdFieldName()` when the public DTO identifier is not named `id`, for example a legacy business key such as `companyCode`. Also keep `getResponseId(...)` aligned in the controller. Otherwise `/schemas/filtered` and Praxis UI may report or consume a divergent `x-ui.resource.idField`.
- Implement `getDatasetVersion()` when the host can provide a cheap stable version such as `EntityName:count` or a real update marker.
- Register option sources only when fields actually need governed entity lookup. Do not publish provider internals in public payloads.
- Treat cursor pagination, locate, and stats according to their actual support model. Cursor pagination has a baseline implementation but still needs runtime proof for sort stability, SQL, and page continuity; override it only for keyset/dialect/performance/domain behavior. `locate` is opt-in and must be implemented when the UI needs jump-to-row or position restoration. Stats require support modes plus `getStatsFieldRegistry()` before claiming `/stats/*` works.
- Add host-specific service methods only for real domain commands or integration behavior that is not covered by the resource baseline. Do not add `buscarPorNome`, `filtrar`, `listarPorStatus`, or similar methods when the same behavior belongs in the `FilterDTO` with `@Filterable`.
- For collection export, do not rely on frontend-provided fields or `maxRows` as authority. The service must declare `supportsCollectionExport()`, return `getCollectionExportCapability()`, enforce server-side field allowlists and row limits, apply the resource filter/security rules, and use the canonical export executor or an equivalent governed engine.
- Validate advertised capabilities against HTTP. Do not rely only on OpenAPI or `/capabilities`; execute `/filter`, `/filter/cursor`, `/locate`, `/stats/*`, `/options/*`, `/export` when supported, `/schemas/filtered`, `/schemas/domain` when available, item/collection capabilities, item surfaces, and item actions for the resource under test.
- For legacy Oracle or other constrained databases, validate generated SQL for pageable filters and stats early. Dialect mismatch is a host integration issue until proven to be a starter defect.

## Semantic Text Rules

- Write `@Operation(summary=..., description=...)` for public resource endpoints when they are explicitly declared in the host. Omission is acceptable for inherited endpoints or not-yet-curated scaffolds only, and should be treated as a documentation gap before the resource becomes a public reference.
- Make summaries and descriptions describe the business operation, real fields/dimensions, constraints, effects, and relationships. Do not describe only the HTTP verb, pagination, or endpoint path.
- `@Schema.description` is domain documentation for each DTO/property. `@UISchema.label` is UI text and must not be used as a source for generated `@Schema` descriptions.
- For `@ResourceIntent`, `@UiSurface`, and `@WorkflowAction`, keep `id`, `title`, `intent`, `tags`, `scope`, and descriptions stable and aligned with the real method, DTO, service behavior, allowed states, and authorities.
- Preserve stable `operationId` when exposed, use OpenAPI tags as real domain grouping, and keep `@ExampleObject` or examples aligned with validation and actual use cases. These values are indexed by catalog/RAG surfaces and should not be filler.
- For fields with privacy, compliance, AI usage, security, finance, identity, or policy relevance, add deliberate `@DomainGovernance`, `AiUsagePolicy`, or `AiUsageMode` metadata and verify it in `x-domain-governance` and `/schemas/domain`.
- Avoid negative descriptions that introduce unrelated domain terms and pollute semantic search. Do not promise fields, workflow effects, permissions, or integrations not implemented by the endpoint.

## Tests

For a new resource, prefer at least:

- compile/test phase for mapper and generics correctness;
- Maven dependency resolution against the artifact repository used by the host;
- a schema smoke for the create or filter DTO when runtime proof is in scope;
- a resource filter or options smoke when the UI/runtime will consume it immediately.
