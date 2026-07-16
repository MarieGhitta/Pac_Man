# Git Cheat Sheet — Workflow collaboratif

> Règle d'or : on ne push **jamais** directement sur `main`. Branches courtes, PR petites, review systématique.

---

## Cycle complet d'une feature

```bash
# 1. Partir d'un main à jour
git switch main
git pull origin main

# 2.a Créer sa branche
git switch -c feat/ast-chunker
git checkout -b <nom_de_la_branche>

# 2.b Changer de branche
git checkout <nom_de_la_branche>

# 3. Bosser + committer par petits paquets
git add src/chunkers/ast_chunker.py
git commit -m "feat: AST-based chunker for Python files"
git add tests/test_ast_chunker.py
git commit -m "test: unit tests for AST chunker"
# ... etc, autant de commits que d'étapes cohérentes

# 4. Se resync avec main avant de pousser
git fetch origin
git rebase origin/main          # ou: git merge origin/main

# 5. Pousser
git push -u origin feat/ast-chunker

# 6. Ouvrir la PR sur l'interface web → review → CI verte → merge (squash)

# 7. Nettoyer
git switch main
git pull origin main
git branch -d feat/ast-chunker
```

---

## Convention de nommage des branches

| Préfixe      | Usage                          |
|--------------|--------------------------------|
| `feat/`      | nouvelle fonctionnalité        |
| `fix/`       | correction de bug              |
| `refactor/`  | réécriture sans changer le comportement |
| `docs/`      | documentation                  |
| `test/`      | ajout / correction de tests    |

## Messages de commit — Conventional Commits

Format : `<type>[scope optionnel]: <description>`

```
feat: add AST-based splitter
fix(bm25): correct off-by-one in scoring
feat(api)!: change retriever signature   # ! = breaking change
```

| Type        | Usage                                      |
|-------------|--------------------------------------------|
| `feat:`     | nouvelle fonctionnalité                    |
| `fix:`      | correction de bug                          |
| `refactor:` | réécriture sans changer le comportement    |
| `docs:`     | documentation                              |
| `test:`     | ajout / correction de tests                |
| `chore:`    | maintenance (deps, config, build…)         |
| `perf:`     | optimisation de perf                       |
| `style:`    | formatage, pas de changement logique       |
| `ci:`       | config CI/CD                               |

- À l'impératif présent : `Add`, `Fix`, `Refactor`, pas `Added` / `wip` / `fix stuff`
- Une ligne de résumé claire (~50 car.), détails dans le corps si besoin
- Un commit = un changement cohérent qui compile / passe les tests

---

## Commandes du quotidien

```bash
git status                      # où j'en suis
git diff                        # changements non stagés
git diff --staged               # changements stagés
git add -p                      # stager par morceaux (choisir quoi committer)
git switch -                    # revenir à la branche précédente
git log --oneline --graph --all # historique visuel
git restore <file>              # annuler modifs non stagées d'un fichier
git restore --staged <file>     # unstager un fichier
```

## Rebase & résolution de conflits

```bash
git fetch origin
git rebase origin/main
# → conflit : éditer les fichiers, puis
git add <fichier_résolu>
git rebase --continue
# → pour tout annuler et repartir
git rebase --abort
```

## Push force (sur SA branche uniquement)

```bash
git push --force-with-lease     # ✅ sûr : refuse d'écraser le travail d'un autre
git push --force                # ❌ jamais (écrase aveuglément)
```

---

## Rebase vs Merge (étape 4)

| | `rebase origin/main` | `merge origin/main` |
|---|---|---|
| Historique | linéaire, propre | commits de merge |
| Réécrit l'historique | oui | non |
| Simplicité | moyen | simple |
| Sur branche partagée | ⚠️ à éviter | OK |

---

## Interdits absolus

- ❌ Push direct sur `main`
- ❌ `--force` sur `main` ou une branche partagée
- ❌ Réécrire l'historique d'une branche sur laquelle quelqu'un d'autre bosse
- ❌ `git add .` aveugle qui ramasse `__pycache__`, venv, build, `/goinfre`…
- ❌ PR géante de 2000 lignes (personne ne la relit vraiment)

## Réflexes

- ✅ `git pull` avant de commencer à bosser
- ✅ `.gitignore` propre dès le premier commit
- ✅ La CI doit être verte avant tout merge
- ✅ Celui qui ouvre la PR résout ses propres conflits
- ✅ Supprimer la branche après merge
