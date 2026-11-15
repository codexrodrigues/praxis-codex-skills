"""Compile the exact canonical guide snippets and verify their descriptor contract.

No downloads, database or publication. --classpath must identify the real starter
artifact and any runtime dependencies it requires; no mocked Praxis contracts.
"""
import argparse
import hashlib
import os
from pathlib import Path
import re
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--java-home', type=Path, required=True)
    parser.add_argument('--classpath', required=True)
    parser.add_argument('--guide', type=Path, default=Path(__file__).resolve().parents[1] /
                        'codex-skills/praxis-java-host-project/references/resource-baseline.md')
    args = parser.parse_args()
    source = args.guide.read_text(encoding='utf-8-sig')
    blocks = re.findall(r'```java\s*\n(.*?)\n```', source, re.S)

    def block(marker):
        found = [b for b in blocks if marker in b]
        if len(found) != 1:
            raise ValueError(f'Expected one fenced snippet for {marker}, found {len(found)}')
        return found[0]

    paths = block('public final class ApiPaths {')
    config = block('public class HrOptionSourcesConfig {')
    probe = '''
import java.util.*;
import com.example.hr.constants.ApiPaths;
import org.praxisplatform.uischema.options.*;
public class Probe {
    static void check(boolean value, String message) {
        if (!value) throw new AssertionError(message);
    }
    public static void main(String[] args) {
        var registry = new HrOptionSourcesConfig().hrOptionSourceRegistry();
        var source = registry.resolve(Position.class, ApiPaths.HumanResources.POSITION_SOURCE).orElseThrow();
        check(source.type() == OptionSourceType.RESOURCE_ENTITY, "source type");
        check("/api/human-resources/positions".equals(source.resourcePath()), "resource path");
        check("positionLookup".equals(source.key()), "source key");
        check("/api/human-resources/positions/option-sources/positionLookup/options/filter"
            .equals(ApiPaths.HumanResources.POSITION_OPTIONS), "literal baseline");
        check(ApiPaths.HumanResources.POSITION_OPTIONS.equals(source.runtimeContract().filterEndpoint()), "runtime endpoint");
        check("name".equals(source.labelPropertyPath()) && "id".equals(source.valuePropertyPath()), "label/value");
        check(source.dependsOn().equals(List.of("companyId")), "dependsOn");
        var lookup = source.entityLookup();
        check(lookup.dependencyFilterMap().equals(source.dependencyFilterMap()), "dependency mapping");
        check("code".equals(lookup.codePropertyPath()), "code field");
        check(lookup.searchPropertyPaths().equals(List.of("code", "name")), "search fields");
        check(lookup.selectionPolicy() != null && !lookup.selectionPolicy().isEmpty(), "selection policy");
        check(lookup.capabilities().detail() && lookup.capabilities().navigateToDetail(), "detail capabilities");
        check("detail".equals(lookup.detail().surfaceId()) && "position-summary".equals(lookup.detail().previewSurfaceId()), "surfaces");
        check("human-resources.positions".equals(lookup.detail().resourceKey()), "target resource");
        check("directory".equals(lookup.display().preset()) && lookup.display().fields().size() == 2, "display");
        check(lookup.filtering().sortOptions().stream().anyMatch(s -> s.key().equals(lookup.filtering().defaultSort())), "default sort");
        lookup.toMetadataMap();
        System.out.println("PASS: exact guide snippets compile; descriptor contract verified");
    }
}
'''
    # Only framework annotations and the example's domain owner are fixtures.
    # All Praxis classes come from the caller-supplied artifact.
    prelude = '''import java.util.*;
import com.example.hr.constants.ApiPaths;
import org.praxisplatform.uischema.options.*;
@interface Configuration {}
@interface Bean {}
class Position {}
'''
    with tempfile.TemporaryDirectory(prefix='praxis-lookup-guide-') as tmp:
        root = Path(tmp)
        files = {'ApiPaths.java': paths, 'HrOptionSourcesConfig.java': prelude + config, 'Probe.java': probe}
        for name, text in files.items():
            (root / name).write_text(text, encoding='utf-8')
        suffix = '.exe' if os.name == 'nt' else ''
        subprocess.run([str(args.java_home / 'bin' / ('javac' + suffix)), '-encoding', 'UTF-8',
                        '-cp', args.classpath, '-d', tmp, *[str(root / name) for name in files]], check=True)
        subprocess.run([str(args.java_home / 'bin' / ('java' + suffix)), '-cp',
                        tmp + os.pathsep + args.classpath, 'Probe'], check=True)
    print('Guide SHA-256:', hashlib.sha256(args.guide.read_bytes()).hexdigest())
    for entry in args.classpath.split(os.pathsep):
        artifact = Path(entry)
        if artifact.is_file():
            print('Artifact SHA-256:', artifact.name, hashlib.sha256(artifact.read_bytes()).hexdigest())


if __name__ == '__main__':
    main()
