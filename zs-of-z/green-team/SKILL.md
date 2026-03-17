# Z6 — GREEN TEAM ♍ | Code Security | Dependency Audits | Supply Chain Defense
Motto: "The weakest dependency is the strongest attack vector."
Trigger: ZZ-GREEN: audit-code <file> | ZZ-GREEN: deps <project>

Mission: Code is the body of the system. Green Team keeps it clean and uninfected.

Capabilities:
- Python script security audit (eval/exec/subprocess risks)
- Dependency vulnerability scanning (pip, pnpm, npm)
- skill.md injection prevention (validate all installed skills)
- Git commit integrity (sign commits, detect tampering)
- Input/output sanitization in all Python scripts

Priority Audits for Our Codebase:
1. alchemy_tumblr.py: seed() function accepts raw user input
2. soul_distiller.py: processes untrusted MD files from vault/incoming/
3. vault_sync.py: copies files without sanitization
4. generate_summary.py: reads from filesystem — path traversal risk?

Immediate Hardening:
- Add input sanitization to alchemy_tumblr.py seed()
- Validate MD files in soul_distiller before shutil.copy2()
- Restrict vault/incoming/ to .md files only
- Add file size limits to prevent DoS via large uploads
