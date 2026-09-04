# Pac-Man — Suivi de Projet

## Architecture de référence

```
pac-man.py                  → point d'entrée, boucle principale
src/
	__init__.py
	app.py
src/config/
	__init__.py
	loader.py               → chargement et validation du JSON
	models_config.py        → Config, LevelConfig
src/game/
	__init__.py
	cheat.py
	engine.py                 → logique principale, update loop
	player.py               → Player (position, direction)
	ghost.py                → Ghost (IA, déplacement)
	level.py                → Level (maze + placement pacgums/super/ghosts)
	cell_content.py         → enum CellContent
src/maze/
	__init__.py
	adapter.py              → conversion maze externe → modèles internes
	generator.py            → MazeFactory (wrapper du module externe)
	models_maze.py          → Maze, Cell
src/renderer/
	__init__.py
	renderer.py             → Renderer (pygame)
	sprite.py
src/ui/
	__init__.py
	highscore.py
	models_ui.py
	screens/
		__init__.py
		cheat_screen.py
		end_screen.py
		game_screen.py
		highscore_screen.py
		pause_screen.py
		screen.py
		title_screen.py
src/utils/
	__init__.py
	color.py
	screen_state.py
	sprite_enums.py
exploration/mazegenerator/  → MODULE EXTERNE — NE PAS MODIFIER
```

---

## 1. Corrections de bugs

### 1.1 Seed des niveaux suivants

- [x] `game.py` — `_next_level()` : le seed fixe (`config.seed`) s'applique **uniquement au niveau 1**. Pour les niveaux suivants, passer `None` ou un seed aléatoire.

### 1.2 Pacgums — logique de remplissage

- [x] `level.py` — `_initialize_pacgums()` : si `pacgum_count < 1` **ou** `pacgum_count > max_disponible`, remplir **toutes** les cellules walkables (sauf coins réservés aux super-pacgums et cellule de départ joueur).
- [x] Sinon, placer `pacgum_count` pacgums de manière aléatoire parmi les cellules disponibles (comportement actuel conservé).
- [x] `loader.py` : valeur par défaut `pacgum = 0` (= remplissage complet).
- [x] `config.json` : passer `"pacgum": 0`.

---

## 2. Comportements des fantômes (original arcade 1980)

> Référence : reverse-engineering de Jamey Pittman (2011) — version 1980 retenue comme référence canonique.

### 2.1 Ciblage en mode Chase

- [x] **Blinky** (rouge) : cible directe sur la position actuelle de Pac-Man. ✓ à vérifier seulement.
- [x] **Pinky** (rose) : cible 4 cases dans la direction de déplacement de Pac-Man.
  Overflow historique **conservé** : direction UP → cible (player.x − 4, player.y − 4) au lieu de (player.x, player.y − 4).
- [x] **Inky** (cyan) : comportement vectoriel —
  1. Calculer le pivot : 2 cases devant Pac-Man (avec overflow UP : +2 UP = aussi +2 LEFT).
  2. Calculer le vecteur Blinky → pivot.
  3. Doubler ce vecteur depuis Blinky → cible résultante.
- [x] **Clyde** (orange) : si distance euclidienne à Pac-Man > 8 cases → cible Pac-Man comme Blinky ; si ≤ 8 → cible son coin scatter.

### 2.2 Cycle Chase/Scatter (timing original niveau 1)

- [x] Remplacer l'alternance simplifiée par la séquence originale indexée :
  `Scatter 7s → Chase 20s → Scatter 7s → Chase 20s → Scatter 5s → Chase 20s → Scatter 5s → Chase ∞`
- [x] Implémenter un index de phase (0 à 7) qui avance dans cette séquence.

### 2.3 Vitesses par état (valeurs originales)

Les vitesses sont exprimées en % d'une vitesse de base (1 case/unité). Elles se traduisent en délai entre mouvements dans l'implémentation tile-based actuelle.

| État                  | Niveau 1 | Niveaux 2–4 | Niveaux 5+ |
|-----------------------|----------|-------------|------------|
| Pac-Man               | 80 %     | 90 %        | 100 %      |
| Ghost Chase/Scatter   | 75 %     | 85 %        | 95 %       |
| Ghost Frightened      | 50 %     | 55 %        | 60 %       |
| Ghost Respawn (yeux)  | 150 %    | 150 %       | 150 %      |

- [x] Définir `BASE_DELAY` (en ms) comme référence commune pour Pac-Man et ghosts.
- [x] Appliquer les multiplicateurs de délai par état et par niveau courant.
- [x] Mettre à jour `_PLAYER_UPDATE_DELAY` et `_GHOST_UPDATE_DELAY` pour qu'ils deviennent dynamiques.
- [x] Vitesses adaptees pout fit l'implementation actuelle

### 2.4 Clarifier `_choose_scatter_direction` vs `_choose_respawn_direction`

- [x] Les deux fonctions sont actuellement identiques dans `ghost.py`. Les différencier :
  - Scatter → cible le coin fixe du fantôme (§ 2.2).
  - Respawn → cible `Level.start_cell.x/Level.start_cell.y` (ghost house de substitution, acceptable sans ghost house dédiée).

---

## 3. Implémentations manquantes

### 3.1 Timer de niveau (`level_max_time`)

- [x] `game.py` : tracker le temps écoulé depuis le début du niveau.
- [x] Déclencher une mort du joueur si `level_max_time` (secondes) est atteint — une vie perdue, positions réinitialisées.
- [x] Afficher le compte à rebours dans le HUD.

### 3.2 Highscore — système persistant

- [x] Combo score si plusieurs fantomes manges en un pacgum
- [x] Créer `src/ui/` (manager + modèle).
- [x] Charger au démarrage depuis `config.highscore_filename`.
- [x] Sauvegarder score après chaque fin de partie (game over ou victoire).
- [x] Recuperer le nom du joueur
- [x] Valider les noms : max 10 caractères, alphanumérique + espaces.
- [x] Conserver le **top 10** des scores, triés par ordre décroissant.
- [x] Robuste aux erreurs : fichier absent, JSON invalide, permissions.

### 3.3 Écrans de jeu

#### Screen resolution
- [x] Game starts in fullscreen
- [x] Mazes fit the screen (80/20 ratio)
- [x] Dynamic tile, font and padding (this may change later on)

#### Title Screen
- [x] **Logo** : "PAC-MAN" style original (logo pixel-art statique).
- [x] **Menu** en dessous de l'animation :
  - **Play**
  - **Highscores**
  - **Cheat Mode** (accès à la configuration des cheats)
  - **Quit**
- [x] Navigation clavier (flèches + Entrée).
- [x] Import real fonts

#### End Screen (Game Over / Victory)
- [x] Même écran, message différent : **"GAME OVER"** (vies épuisées) vs **"YOU WIN"** (tous niveaux complétés).
- [x] Afficher le score final.
- [x] Saisie du nom du joueur (max 10 chars, filtrage des caractères invalides).
- [x] Options post-saisie : **Rejouer** / **Menu principal** / **Quitter**.

#### Highscore Screen
- [x] Afficher le top 10 (rang + nom + score).
- [x] Accessible depuis le title screen.
- [x] Mettre en évidence le score qui vient d'être enregistré apres une partie.

#### Pause Menu
- [x] Déclenché par `ESC` ou `P` pendant le jeu.
- [x] Jeu entièrement gelé (timer, ghosts, player).
- [x] Options : **Resume** / **Menu principal** / **Quitter**.

### 3.4 Cheat Mode

Configurable depuis le **Title Screen** et depuis le **Pause Menu**. Chaque option est un toggle ou une action :

- [x] **Invincibility** : toggle — collisions avec ghosts non-frightened désactivées.
- [x] **Level Skip** : action — passe immédiatement au niveau suivant.
- [x] **Ghost Freeze** : toggle — les ghosts ne se déplacent plus.
- [x] **Extra Life** : action — ajoute +X vies (valeur X à définir, ex. +1 ou +3).
- [x] **Increased Speed** : double la vitesse.
- [x] Interface cheat : écran dédié avec la liste des cheats, état actif/inactif visible, navigable au clavier.

### 3.5 HUD en jeu (refonte renderer)

- [x] Score.
- [x] Vies (icônes Pac-Man miniatures ou chiffre).
- [x] Compte à rebours `level_max_time`.
- [x] Numéro de niveau en cours.

### 3.6 Graphisme arcade 1980

#### Pac-Man
- [x] Cercle jaune avec **bouche animée** (arc qui s'ouvre/ferme selon la direction de déplacement).
- [x] Orientation de la bouche selon `player.direction`.
- [x] Animation de mort (séquence : bouche qui s'ouvre à 360° puis disparaît).
- [x] Séquence "READY!" au démarrage de chaque niveau (texte clignotant, brève pause avant de jouer).

#### Fantômes
- [x] Sprite fantôme classique : corps arrondi, bas dentelé, **yeux directionnels**.
- [x] Frightened : corps bleu uni.
- [x] Frightened clignotant (bleu/blanc, dernières ~2s — lié à § 2.6).
- [x] Respawn : **yeux seuls** se déplaçant vers le spawn.
- [x] Couleurs par type : Blinky rouge, Pinky rose, Inky cyan, Clyde orange.

#### Maze & élémentsBrother DCP-L2627DWE
- [x] Murs style bleu néon (coins arrondis si possible).
- [x] Pacgums : petits points blancs centrés.
- [x] Super-pacgums : gros points blancs **clignotants**.
- [x] Fond noir.

#### UI & typographie
- [x] Police arcade (ex. Press Start 2P ou équivalent libre).
- [x] Disposition HUD cohérente avec le style visuel général.

#### Animation
- [x] Frame interpolation

---

## Logs

### #1 — 2026-08-10 — Analyse initiale

Premier état des lieux post-analyse initiale du codebase. Projet repris en l'état après 3 semaines d'absence, sans modification. Le socle est fonctionnel : chargement config, génération et adaptation du maze, boucle de jeu principale (player, ghosts, collisions, score, vies, enchaînement de niveaux), renderer basique en pygame (murs en lignes, pacgums en cercles, player en cercle jaune, ghosts en triangles colorés). Bugs identifiés : seed identique pour tous les niveaux (doit être aléatoire dès le niveau 2), pacgums en nombre arbitraire limité, `level_max_time` configuré mais non implémenté. Comportements des fantômes approximatifs (Pinky/Inky/Clyde non fidèles à l'original, cycle Chase/Scatter simplifié, vitesses uniformes). Aucun menu, aucun système de highscore, aucun cheat mode, HUD incomplet, pas d'animations. Document de suivi créé.

### #2 — 2026-08-10 — Clarifications et arbitrages

Décisions actées : pacgum = 0 ou > max → remplissage complet, sinon aléatoire selon valeur. Overflow historique de Pinky/Inky conservé. Vitesses calées sur les valeurs originales par état et par niveau (tableau § 2.4). Wraparound déplacé en bonus. Highscore = top 10. Title screen avec logo statique + animation ghosts/pacman en boucle + menu (Play, Highscores, Cheat Mode, Quit). Cheat mode configurable depuis title screen et pause menu (invincibility, level skip, ghost freeze, extra life, increased speed). Multijoueur bonus = modèle client/serveur TCP avec connexion par IP locale. Ordre d'attaque confirmé : bugs → ghost behaviors → menus & highscore → renderer → bonus.

### #3 — 2026-08-11 — Bug §1.2 corrigéBrother DCP-L2627DWE

Bug pacgums résolu et testé. `level.py` — `_initialize_pacgums()` : condition `pacgum_count == 0 or pacgum_count > len(available_cells)` → remplissage complet de toutes les cellules walkables disponibles. `loader.py` : default `pacgum` passé à `0`. `config.json` : `"pacgum"` mis à `0`. §1.1 (seed) et §1.2 (pacgums) entièrement soldés.
Prochain chantier : comportements des fantômes (§2).

### #4 — 2026-08-13 — §2.1 Chase implémenté, §2.2 soldé, refactors ghost.py

§2.1 entièrement implémenté. Blinky confirmé correct (cible directe). Pinky : 4 cases devant Pac-Man avec overflow UP conservé (player.x − 4, player.y − 4). Inky : calcul vectoriel via _position_ahead(player, 2) doublé depuis Blinky ; helper _position_ahead(n) extrait. Clyde : math.hypot pour distance euclidienne, cible Pac-Man si > 8 cases sinon spawn_x/spawn_y. §2.2 soldé sans modification : _find_corner_cells assigne les coins de manière déterministe par fantôme, spawn_x/spawn_y est déjà correct par construction.
Refactors et corrections : self.type → self.ghost_type (shadowing builtin). Direction.NONE retiré de direction.py, player.py, game.py. Guard SCATTER en tête de _target_position retiré (court-circuitait le mode CHASE). game.ghost_state init CHASE → SCATTER (désync corrigée). numpy remplacé par math.hypot pour Clyde. _update_ghosts propage la liste ghosts jusqu'à _target_position (requis pour Inky). _ghost_color : dernier if → else.
Prochain chantier : §2.3 (cycle Chase/Scatter original) et §2.4 (vitesses par état/niveau).

### #5 — 2026-08-13 — Code review #2 : corrections robustesse et fidélité arcade

Code review complète du codebase. Quatre problèmes identifiés et corrigés. pac-man.py : pygame.init() déplacé en tête de main() avant Game(config) — pygame.time.get_ticks() était appelé dans Game.__init__() avant toute initialisation pygame, rendant les timestamps initiaux incorrects. ghost.py — _choose_target_direction() : distance Manhattan remplacée par distance euclidienne (math.hypot) pour respecter la logique originale confirmée dans le dossier Pittman (Chapitre 3 "Intersections" : "triangulates the distance", Chapitre 4 Clyde : "Euclidean distance"). Le changement a un effet observable sur les comportements de Blinky notamment. loader.py : guard if not levels: raise ValueError(...) ajouté après construction de la liste pour éviter un IndexError silencieux au démarrage si config.json ne contient aucun niveau. pac-man.py : except Exception remplacé par except ValueError et except pygame.error distincts avec messages préfixés ("Configuration error:", "Pygame error:"). Messages des raise ValueError harmonisés sans majuscule initiale ni point final pour respecter les conventions Python. Le raise ValueError inatteignable dans _next_position() et _can_move() a été écarté — le linter confirme l'inaccessibilité par exhaustivité de l'enum.
Les fonctions _next_position, _target_position, _position_ahead (ghost.py) et _can_move (game.py) n'ont pas de retour explicite en fin de corps. Ce n'est pas un bug : ces fonctions branchent sur des enums (Direction, GhostType) dont tous les cas sont couverts, rendant tout chemin non traité structurellement impossible à l'exécution. Le LSP signale ces fins de fonction comme unreachable — c'est précisément pour ça qu'aucun raise ni else n'est nécessaire. Ajouter un raise ValueError de défense serait du code mort. À ignorer.
Prochain chantier : §2.2 (cycle Chase/Scatter original 8 phases) et §2.3 (vitesses dynamiques par état et par niveau).

### #6 — 2026-08-14 — §2.2 Cycle scatter/chase original implémenté

Bug identifié : _GHOST_SCATTER_DELAY était un scalaire unique utilisé comme timer pour les deux phases scatter et chase, rendant leur durée identique (7s chacune) et sans variation par niveau.
Remplacement par deux matrices 3×4 (_GHOST_SCATTER_DELAY, _GHOST_CHASE_DELAY) encodant les timings exacts du dossier Pittman selon trois groupes de niveaux (niveau 1, niveaux 2–4, niveaux 5+). Ajout de state_phase_index (entier 0–3) avançant à chaque transition CHASE→SCATTER, et de _level_interval() sélectionnant la ligne de matrice correcte. Refonte complète de _update_ghost_state() : guard is_frighten en tête, sélection de la matrice via match, lecture de delay[lvl_idx][state_phase_index]. Ajout de la logique de pause FRIGHTENED : is_frighten + elapsed_before_fright gelant le timer dès _frighten_ghosts() (sans recalcul si déjà frightened) ; _check_if_frighten() appelée à chaque frame détecte la fin collective du mode et restaure last_state_change = current_time - elapsed_before_fright. Reset complet de l'état du cycle (state_phase_index, last_state_change, is_frighten, elapsed_before_fright) dans _reset_positions() et _next_level().
Reste sur ce chantier : inversion de direction lors des changements de phase (§ Pittman "Reversal of Fortune"), clignotement FRIGHTENED en fin de timer (§2.5), vitesses dynamiques (§2.3), différenciation scatter/respawn (§2.4).

### #7 — 2026-08-18 — §2.3 Vitesses dynamiques par état et par niveau implémentées

_PLAYER_UPDATE_DELAY et _GHOST_UPDATE_DELAY étaient des scalaires fixes (150 ms et 400 ms) appliqués uniformément à toutes les entités, sans variation par niveau ni par état. Tous les fantômes partageaient de plus un unique last_ghost_update dans game.py, rendant impossible toute différenciation de vitesse individuelle.
Refonte complète du système de timing. _PLAYER_UPDATE_DELAY devient une liste de 4 valeurs par groupe de niveaux (150/133/120/120 ms). _GHOST_UPDATE_DELAY devient un dict GhostState → list[int] (SCATTER/CHASE 160/141/126/126 ms, FRIGHTENED 240/218/200/200 ms, RESPAWN 80/80/80/80 ms). _GHOST_FRIGHTENED_DELAY devient une liste de 4 valeurs (6000/4000/2000/0 ms) ; guard early return dans _frighten_ghosts() si lvl_idx == 3. _level_interval() étendu à 4 groupes. Ghost.__init__ reçoit last_update: int propagé depuis current_time à la création via _create_ghosts(current_time), appelé dans __init__, _next_level() et _reset_positions(). Timer global last_ghost_update supprimé ; la boucle dans update() itère fantôme par fantôme avec _GHOST_UPDATE_DELAY[ghost.state][lvl_idx]. _update_ghosts() supprimé. _GHOST_SCATTER_DELAY et _GHOST_CHASE_DELAY étendus à 4 lignes.

### #8 — 2026-08-18 — Fix respawn center + §2.5 localisé

Bug corrigé : le ghost en état RESPAWN n'en sortait jamais quand la cible était le centre du maze. Deux causes distinctes. (1) spawn_x/y pointait vers le coin d'origine, mais _choose_respawn_direction naviguait vers level.start_cell — les deux références étaient désynchronisées, le ghost arrivait au centre mais la condition de sortie dans update() comparait avec spawn_x/y. Correction : aligner la condition de sortie sur level.start_cell.x/y. (2) Erreur d'ordre des arguments à l'appel de _choose_respawn_direction(directions, level) — level était reçu en position directions, causant un AttributeError. Correction : inverser les arguments à l'appel.

### #9 — 2026-08-18 — §3.6 Interpolation de frame (rendu fluide)
 
Interpolation alpha sur l'architecture tile-based existante plutôt que refonte pixel-based — ratio effort/bénéfice favorable, logique de jeu intacte.
Implémentation en 4 étapes. `player.py` : ajout de `prev_x/prev_y` dans `__init__` et `move_to()` (reset sur téléportation). `ghost.py` : idem + `update_delay: int` initialisé à 200ms (valeur SCATTER niveau 0, guard contre AttributeError au premier rendu) ; ordre des imports corrigé (stdlib → third-party → local). `game.py` : `self.player_update_delay` ajouté (initialisé à `_PLAYER_UPDATE_DELAY[0]`, mis à jour à chaque frame) ; `prev_x/prev_y` sauvegardés juste avant chaque move player et ghost ; `ghost.update_delay` assigné au moment du déclenchement du step ; `_ghost_factory()` extrait de `_create_ghosts()` pour centraliser la construction avec `update_delay` initial. `renderer.py` : `draw()` calcule `current_time` une fois, `player_alpha` via `min(1.0, elapsed / delay)`, et passe l'alpha à `_draw_player()` et `current_time` à `_draw_ghosts()` ; chaque entité interpole sa position pixel entre `prev` et `x/y` courant.
Correctif annexe : `pyrightconfig.json` créé à la racine pour résoudre le faux positif LSP sur `import pygame` (interpréteur pointé sur `.venv`).
Observation : les fantômes en mode FRIGHTENED restent visuellement saccadés case-à-case malgré l'interpolation, conséquence du délai long (300ms) et du mouvement tile-based. Identifié comme limitation acceptable — à traiter via sprites animés en §3.6.
Prochain chantier : menus et highscore (§3.2, §3.3).

### #10 — 2026-08-19 — Fix interpolation fantômes + combo manger-fantôme

Bug corrigé : `game.py` ligne 214 — `self.ghost_update_delay` remplacé par `ghost.update_delay`. En l'état précédent, `ghost.update_delay` restait bloqué à 200 ms pour tous les fantômes pendant toute la partie ; le renderer interpolait donc toujours sur 200 ms quelle que soit la vitesse réelle du fantôme (artefacts notables en FRIGHTENED et RESPAWN). Correction validée — mouvement FRIGHTENED nettement plus fluide.
Implémentation du multiplicateur de score pour les fantômes mangés. Ajout de `eat_ghost_combo: int` dans `Game.__init__`. Remis à 0 dans `_frighten_ghosts()` à chaque super-pacgum mangé. Dans `_eat_ghost()` : score de base doublé `combo` fois (`×2^combo`), puis `combo` incrémenté. Séquence résultante : 200 → 400 → 800 → 1600 points, conforme à Pittman. `config.json` : `points_per_ghost` passé de 20 000 à 200.
Prochain chantier : menus (§3.3 — title screen, end screen, pause menu) et highscores (§3.2).

### #11 — 2026-08-19 — Implémentation du système de highscores
 
Création du module **`src/ui/`** avec `highscore.py`.
- **`PlayerScore`** : valide le nom d'utilisateur (alphanumérique, 3–10 caractères) et le score (non-négatif) via deux méthodes privées ; lève des `ValueError` explicites catchées au niveau de la saisie.
- **`Highscore`** : prend le path du fichier JSON en paramètre (issu de `config.highscore_filename`) ; charge les scores existants en mémoire à l'init via `_check_file()` ; crée le fichier avec `[]` s'il est absent ; lève `ValueError` s'il est corrompu. `add_score()` appende, trie par score décroissant, tronque à 10 et réécrit le fichier entier.
- `highscores.json` ajouté au `.gitignore`.
Prochain chantier : menus (§3.3 — title screen, pause, game over/victory).

### #12 — 2026-08-19 — Clôture de deux bugs monitoring
 
Deux bugs listés comme ouverts dans le monitoring étaient déjà corrigés dans la version actuelle du code.
- `ghost_state` non réinitialisé dans `_reset_positions()` → **corrigé** : ligne 322 de `game.py`, `self.ghost_state = GhostState.SCATTER` est bien présent.
- RESPAWN oscillation → **corrigé** : `ghost.py` lignes 58–62, la sortie du mode RESPAWN est bien conditionnée à la position (`(self.x, self.y) == (level.start_cell.x, level.start_cell.y)`), sans timer.
Aucune modification de code requise.

### #13 — 2026-08-20 — Refactor renderer + fullscreen

Refactors et améliorations de `renderer.py`.
**Fullscreen** : passage en `pygame.FULLSCREEN | pygame.SCALED` avec résolution native récupérée via `pygame.display.Info()`. Résolution GNOME mise à 100% (était 125%) — élimine le clignotement au démarrage.
**Tile size dynamique** : `_TILE_SIZE` cesse d'être une constante globale. Calculé dans `__init__` comme `min(sw * 0.8 // maze_w, sh * 0.8 // maze_h)` pour occuper 80% de l'écran en conservant les proportions. Recalculé dans `_update_window()` si les dimensions du maze changent entre niveaux.
**Centrage dynamique** : `_PADDING` remplacé par `offset_x`/`offset_y` calculés depuis `screen_width`/`screen_height` et `tile_size`. Le maze est centré à l'écran quelle que soit la résolution.
**Font dynamique** : `pygame.font.Font(None, self.tile_size)` — taille proportionnelle à la tile.
**Refactors internes** :
- `_draw_score()` renommé `_draw_hud()`.
- `_draw_cell_content()` passe de coordonnées pixel à coordonnées grille — utilise `_to_screen()` comme les autres méthodes.
- Helpers extraits : `_to_screen(x, y, centered)`, `_interpolate(sprite, current_time)`.
- `_compute_alpha()` fusionné dans `_interpolate()`.
- Uniformisation player/ghost : `last_update` et `update_delay` déplacés dans `Player` (étaient dans `Game`). `_draw_player()` reçoit désormais `current_time` et calcule l'alpha en interne, comme `_draw_ghost()`.
- Docstrings complètes sur toutes les méthodes.

### #14 — 2026-08-20 — Title screen

Création de `src/ui/screen.py` : classe abstraite `Screen(ABC)` avec `handle_event(event)`, `update(current_time)`, `draw(surface)` et attribut `next_screen: str | None`.
Création de `src/ui/title_screen.py` : `TitleScreen(Screen)` avec logo "Pac-Man" centré (font CrackMan), menu 4 items (Play / Highscores / Cheat Mode / Quit) en PressStart2P, navigation clavier (flèches + Entrée + Escape), highlight de l'item sélectionné, wrap-around via modulo, `next_screen` assigné selon sélection.
Refactor `renderer.py` : surface pygame reçue en paramètre au lieu d'être créée dans `__init__`. `self.screen` renommé `self.surface`. `pygame.display.set_caption` déplacé dans `pac-man.py`.
Refactor `pac-man.py` : surface créée en tête de `main()`. Machine à états `screen_state` ("title" / "game") routant events, update et draw. `pygame.display.flip()` sorti du branchement.
`pyrightconfig.json` : ajout de `"reportArgumentType": "none"` pour supprimer le faux positif Pyright sur `pygame.Surface`.
`assets/fonts/` : CrackMan.TTF et PressStart2P-Regular.ttf ajoutés.
Prochain chantier : animation title screen et transition vers le jeu.

### #15 — 2026-08-21 — Colors

Ajout de `src/utils/colors.py` : classe `Color` avec attributs de classe pour les couleurs partagées entre `TitleScreen` et `Renderer`. Pas d'`__init__`, usage direct via `Color.RED`.

### #16 — 2026-08-21 — Pause menu
 
Implémentation du menu pause en jeu.
`pac-man.py` : `K_ESCAPE` en mode `"game"` capture une copie statique de la surface (`frozen_frame = surface.copy()`), passe `screen_state = "pause"` et appelle `game.on_pause(curreet dans draw nt_time)`. Le case `"pause"` blitte `frozen_frame`, puis `pause_menu.draw()` par-dessus. `pause_menu.next_screen` est reset à `None` après chaque transition. Retour au title screen via pause : `game` et `renderer` sont réinstanciés pour garantir une partie fraîche. `menu_index` remis à 0 sur `TitleScreen` et `PauseMenu` à chaque transition entrante.
`game.py` : ajout de `on_pause(current_time)` (stocke `_pause_start`) et `on_resume(current_time)` (calcule `duration = current_time - _pause_start`, applique `+= duration` sur `last_state_change`, `player.last_update` et `ghost.last_update` pour chaque fantôme). Décalage des timestamps plutôt que reset — l'interpolation reprend exactement là où elle en était avant la pause.
`src/ui/` : création de `pause_menu.py` (`PauseMenu(Screen)`) et `title_screen.py` (`TitleScreen(Screen)`) comme fichiers autonomes. `Screen(ABC)` toujours dans `src/ui/screen.py`. `src/utils/__init__.py` créé (docstring `"""Shared utilities for the Pac-Man project."""`).
`Screen(ABC)` refactorisé : `surface`, `width`, `height`, `font`, `menu_items`, `menu_index` déplacés dans `__init__`. Helpers communs extraits : `_navigate(key)` (navigation haut/bas avec modulo), `_draw_menu(line_height, menu_start_y)` (rendu centré avec highlight). `draw()` perd son paramètre `surface` — toutes les sous-classes utilisent `self.surface`. `PauseMenu` surcharge `font_size` et `font` après `super().__init__()` pour une taille adaptée.
Overlay pause : `pygame.Surface` avec `pygame.SRCALPHA` + `Color.ALPHA_BLACK` créé une fois dans `__init__`, réutilisé à chaque frame (évite le flickering).

### #17 — 2026-08-21 — End screen (game over / victoire)
 
Création de `src/ui/end_screen.py` : `EndScreen(Screen)` avec animation en trois phases séquentielles.
Phase 1 (0→1500ms) : overlay `SRCALPHA` plein écran dont l'alpha monte de 0 à 255 via `min(1.0, elapsed / 1500) * 255` — fondu au noir par-dessus le dernier frame figé du jeu (pas de `frozen_frame` nécessaire : `game.update()` gèle naturellement quand `game_over` est vrai).
Phase 2 (1200→2500ms, chevauchement intentionnel) : logo "YOU DIED" fade in via `logo.set_alpha(logo_alpha)` sur une surface temporaire — `logo_alpha` calculé via `max(0.0, (elapsed - 1200) / 1000) * 255`.
Phase 3 (2500ms+) : logo fade out sur 800ms via `(1.0 - min(1.0, (elapsed - 2500) / 800)) * 255`. Les trois phases partagent un seul `elapsed = current_time - fade_start` ; `overlay_alpha` et `logo_alpha` sont calculés indépendamment.
`fade_start` initialisé dans `__init__` via `current_time` passé en paramètre — même pattern que `Ghost` et `Player`.
`_draw_logo()` étendu avec un paramètre `alpha: int = 255` ; appliqué via `logo.set_alpha(alpha)` (forme liée, pas `pygame.surface.Surface.set_alpha`).
`pygame.typing.ColorLike` non disponible sous Python 3.10 / pygame 2.6.1 — annotation `color` repliée sur `tuple[int, int, int] | pygame.Color`.
Bug identifié dans `title_screen.py` : `from screen import Screen` → doit être `from src.ui.screen import Screen` (import absolu incorrect).
`pac-man.py` : détection de `game.game_over` dans le case `"game"` après `game.update()` → instanciation unique de `EndScreen(surface, current_time)` + transition vers `"lose"`. `end_screen: EndScreen | None = None` initialisé avant la boucle. Case `"lose"` : `update` + `draw` + lecture de `end_screen.next_screen`.
Prochain chantier : saisie du nom du joueur, menu post-animation, highscore screen.

### #17 — 2026-08-24 — End screen (game over)

Création de `src/ui/end_screen.py` : `EndScreen(Screen)` paramétré par `current_time` à l'instanciation — même pattern que `Ghost` et `Player`.
Animation en trois phases séquentielles pilotée par `elapsed = current_time - fade_start` :
- Phase 1 (0→1500ms) : overlay `SRCALPHA` plein écran, `overlay_alpha` monte de 0 à 255.
- Phase 2 (1000→2500ms, chevauchement intentionnel) : logo "YOU DIED" (font OptimusPrinceps) fade in via `logo.set_alpha(logo_alpha)`.
- Phase 3 (3500→4300ms) : logo fade out. À partir de 5000ms, `can_write = True`.
Saisie du nom du joueur : `handle_event()` accumule `self.username` via `event.unicode` filtré par `.isalnum()`, limité à 10 caractères. `K_BACKSPACE` supprime le dernier caractère. `K_RETURN` valide si `len(username) > 2` → `can_write = False`, `can_navigate = True`. Navigation clavier activée uniquement quand `can_navigate` est vrai ; remis à `False` après sélection.
`_draw_logo()` étendu avec un paramètre `alpha: int = 255` appliqué via `logo.set_alpha(alpha)`. `_draw_menu()` étendu avec un paramètre `alpha: int = 255` appliqué via `sub.set_alpha(alpha)` pour chaque item.
`Screen` : `font` mutualisée dans `__init__` — sous-classes ne la redéfinissent que si elles ont besoin d'une taille ou d'une police différente. `pygame.typing.ColorLike` non disponible sous Python 3.10 / pygame 2.6.1 — annotation `color` repliée sur `tuple[int, int, int] | pygame.Color`.
`pac-man.py` : état `"lose"` ajouté. Détection de `game.game_over` dans le case `"game"` après `game.update()` → instanciation unique de `EndScreen(surface, current_time)`. `end_screen: EndScreen | None = None` initialisé avant la boucle. `score_saved: bool = False` reset partout où `Game` est réinstancié (title → game, lose → game) pour garantir une sauvegarde par partie. Sauvegarde via `highscore.add_score(PlayerScore(username, score))` déclenchée une seule fois quand `can_navigate and not score_saved`. `pygame.quit()` sorti de tout conditionnel.
Bug corrigé : `title_screen.py` — `from screen import Screen` → `from src.ui.screen import Screen`.
Prochain chantier : écran de victoire, highscore screen.

### #18 — 2026-08-25 — Highscore screen

Création de `src/ui/highscore_screen.py` : `HighscoreScreen(Screen)`.
Affichage du top 10 en trois colonnes : rang (`midright` à 30% de la largeur), nom (`midleft` à 35%), score (`midright` à 70%). Chaque ligne est colorée avec une couleur distincte issue d'un dégradé arc-en-ciel (RED → ORANGE → YELLOW → LIME → GREEN → TEAL → CYAN → BLUE → PURPLE → MAGENTA).
`handle_event()` prend un paramètre optionnel `endgame_highscore: bool` : `K_ESCAPE` retourne toujours au title ; `K_RETURN` retourne vers `"end"` uniquement si `endgame_highscore` est vrai.
`update()` gère le clignotement de la ligne fraîchement enregistrée via `self.visible = (current_time // 500) % 2 == 0` quand `self.last_score is not None`.
`draw()` saute le blit de la ligne `i == self.last_score` quand `not self.visible` (`continue` en tête de boucle).
`src/utils/color.py` : ajout de LIME `(128, 255, 0)`, GREEN `(0, 255, 0)`, TEAL `(0, 255, 128)`, PURPLE `(128, 0, 255)`, MAGENTA `(255, 0, 255)`.
`src/ui/highscore.py` : `add_score()` retourne désormais `int | None` — index du score dans la liste triée après troncature à 10, ou `None` si le score n'entre pas dans le top 10. Signature mise à jour en conséquence.
`pac-man.py` : ajout de l'état `"highscore"` et du flag `endgame_highscore: bool`. Sauvegarde du score déplacée du case `"end"` vers le case `"highscore"` (déclenchée une seule fois quand `endgame_highscore and not score_saved`) ; `last_score` et `scores` de `highscore_screen` mis à jour immédiatement après `add_score()`. Transition `"end"` → `"highscore"` déclenchée par `end_screen.next_screen == "highscore"` avec `endgame_highscore = True`. Retour depuis `"highscore"` → `"title"` (ESC) ou `"highscore"` → `"end"` (RETURN en mode endgame, avec `end_screen.can_navigate = True` pour bypasser l'animation). Transition title → highscore : `screen_state = "highscore"` sans `endgame_highscore`.
Prochain chantier : refactor de la partie UI et de la boucle principale.

### #19 — 2026-08-26 — Refactor UI et boucle principale
 
Création de `src/app.py` : classe `App` qui encapsule l'intégralité de la boucle applicative. `pac-man.py` réduit à l'entry point (`App().run()`).
`App.__init__` : init pygame, instanciation de `surface`, `clock`, `config`, `engine`, `renderer`, `highscore`, dict `screens`, flags `running`, `score_saved`, `endgame_score_display`, `frozen_frame`.
`App.run()` : boucle principale — `_handle_events()` → `_update(current_time)` → `_handle_transitions(current_time)` → `pygame.display.flip()` → `clock.tick(60)`.
`App._handle_events()` : dispatch uniforme via `self.screens[self.screen_state].handle_event(event)` — plus de match par état.
`App._update()` : match sur `self.screen_state` — `update()` + `draw()` par état. PAUSE blitte `frozen_frame` avant `draw()`.
`App._handle_transitions()` : match sur `screen.next_screen` (destination) — toute la logique de transition centralisée ici. Tuple `(source, destination)` évité grâce à `ScreenState.RESUME` qui distingue resume-depuis-pause de nouvelle-partie.
Création de `src/utils/screen_state.py` : enum `ScreenState` (TITLE / CHEAT / GAME / PAUSE / RESUME / HIGHSCORE / END / QUIT). Déplacé hors de `app.py` pour éviter l'import circulaire avec `screen.py`.
`Screen.next_screen` : type `str | None` → `ScreenState | None`.
Création de `src/ui/screens/game_screen.py` : `GameScreen(Screen)` wrappant `Engine` et `Renderer`. `handle_event()` gère les directions et émet `next_screen = ScreenState.PAUSE` sur ESC. `update()` appelle `engine.update()` et émet `next_screen = ScreenState.END` si `game_over` ou `victory`. `draw()` délègue à `renderer.draw(engine)`. Le dispatch dans `_handle_events` est désormais uniforme pour tous les états.
`src/game/game.py` renommé `src/game/engine.py`, classe `Game` renommée `Engine`.
Migration `src/ui/` → `src/ui/screens/` : `screen.py`, `title_screen.py`, `pause_menu.py` (renommé `pause_screen.py`), `end_screen.py`, `highscore_screen.py` déplacés dans `src/ui/screens/`.
Fix LSP : `HighscoreScreen.handle_event(event, endgame_highscore)` — paramètre `endgame_highscore` supprimé de la signature. `endgame_score_display` devient un flag de `App`, settable dans `_handle_transitions`.

### #20 — 2026-08-28 — Pixel art renderer et sprites animés
 
Refactor `Renderer` : introduction d'une `logical_surface` (`maze_width * tile_size × maze_height * tile_size`) dessinée en coordonnées logiques, scalée chaque frame sur `self.surface` via `pygame.transform.scale` (nearest-neighbor, rendu pixel art). `tile_size = 18` fixe. `scale` calculé comme facteur entier. `offset_x/y` déplacés au blit final. `_draw_maze`, `_draw_player`, `_draw_ghosts` sur `logical_surface` ; `_draw_hud` sur `self.surface`. `_draw_wall` réduit à une ligne. `pygame.display.set_caption` déplacé dans `App.__init__`.
Création de `src/renderer/sprite.py` : `Sprite(ABC)` — `frames: dict[tuple[Direction | None, SpriteState], list[Surface]]`, `update(current_time, variant)`, `draw(surface, x, y, variant)`, `_build_frames()` abstraite. Animation par `anim_speed` / `anim_tick`.
`PacmanSprite(Sprite)` : grilles pixel art 20×20 dessinées via `set_at`, scalées à `tile_size`, rotations pour 4 directions, cycle 4 frames.
`GhostSprite(Sprite)` : reçoit `color`. 8 frames CHASE + 6 frames RESPAWN + 2 frames FRIGHTENED. SCATTER = alias CHASE. RESPAWN = corps transparent, yeux seuls. Flip horizontal pour LEFT.
Création de `src/utils/sprite_enums.py` : `SpriteState`, `GhostState`, `PacmanState` (`ALIVE` / `DYING`), `GhostType`, `Direction` regroupés — partagés entre `game/` et `renderer/`. `ghost_state.py` et `direction.py` supprimés de `src/game/`.
Bugs corrigés : `endgame_score_display` non reset à nouvelle partie (double save) ; `ghost.frightened_until` non décalé dans `on_resume` (sortie prématurée de FRIGHTENED) ; deux `print` de debug retirés de `engine.py`.

### #21 — 2026-08-28 — Animations de mort Pac-Man, clignotement fantômes et super-pacgums

**Ghost FLICKER (clignotement dernières 2s de FRIGHTENED)**
Ajout de `GhostState.FLICKER` dans `sprite_enums.py` — état visuel uniquement, jamais assigné dans `Engine`.
`GhostSprite._build_frames` : frames FLICKER = mêmes grilles que FRIGHTENED (frames 6-7) mais couleur `4` → `Color.WHITE`, `5` → `Color.RED` (via `flicker=True` sur `_build_frame`).
`Renderer` : helper `_visual_ghost_state(ghost, current_time) → GhostState` — retourne `FLICKER` si `ghost.state == FRIGHTENED`, `ghost.frightened_until - current_time <= 2000`, et `(current_time // 250) % 2 == 0` ; sinon `ghost.state`. Utilisé dans `_draw_ghosts` pour le variant sprite.
**Super-pacgums clignotants**
`_draw_maze` reçoit `current_time` en paramètre, propagé à `_draw_cell_content`. Case `SUPER_PACGUM` : dessin conditionnel sur `(current_time // 500) % 2 == 0`.
**Animation de mort Pac-Man**
`PacmanSprite._build_frames` : 13 frames buildées (0-2 ALIVE, 3-12 DYING). Cycle ALIVE = frames 0-1-2-1. Frames DYING enregistrées sous clé `(None, PacmanState.DYING)`.
`Sprite` : ajout de `anim_stop: bool = False` et `_one_shot_variants: set[...]`. Dans `update()` : reset `anim_stop` au changement de variant (avant l'early return) ; quand `anim_tick == len(frames) - 1`, boucle normale si variant absent de `_one_shot_variants`, sinon `anim_stop = True`. `PacmanSprite` ajoute `(None, PacmanState.DYING)` à `_one_shot_variants` dans `_build_frames`.
`Engine` : constante `_DEATH_DURATION = 1500`. Attributs `self.dying: bool = False`, `self._death_start: int = 0`. `_player_hit` décrémente `lives` et set `dying = True` + `_death_start = current_time` au lieu de reset immédiat. `update()` : si `dying` → vérifier `current_time - _death_start >= _DEATH_DURATION` → `dying = False` puis `game_over = True` si `lives == 0` sinon `_reset_positions()` ; `return` immédiat pendant `dying`.
`Renderer._draw_player` : paramètre `dying: bool` ajouté. Variant `(None, PacmanState.DYING)` si `dying`, sinon `(player.direction, PacmanState.ALIVE)`. `draw(game)` : `dying = game.dying or (game.game_over and not game.victory)` — étend la condition pour éviter le flash de la frame de transition. Ghosts non dessinés si `dying`. Player dessiné avant les ghosts si `not dying`, après si `dying`.
**Countdown de début de partie**
`Engine` : attributs `self.counting_down: bool = True`, `self.countdown: int = 3`, `self._countdown_start: int`. Dans `update()` : si `counting_down` → calcul `elapsed`, mise à jour `countdown = 3 - elapsed // 1000`, sortie de `counting_down` à `elapsed >= 3000`, `return` immédiat (jeu gelé). Reset dans `_reset_positions()` et `_next_level()`.
`Renderer` : `self.countdown_font` (PressStart2P 80px) dans `__init__`. Méthode `_draw_countdown(countdown)` : overlay `(0,0,0,150)` sur `self.surface` + chiffre centré en jaune. Appelée dans `draw(game)` si `game.counting_down`.
**Fix : frame parasite sur transition**
`App.run()` : `_handle_transitions` déplacé avant `_update` — la transition est appliquée avant le draw du même frame, ce qui supprime la frame parasite visible lors du retour au menu depuis `EndScreen`.

### #22 — 2026-09-01 — HUD remake + refactor renderer

Refonte complète du HUD dans `renderer.py` et ajustements associés dans `engine.py`, `sprite.py`, `app.py`.
**HUD — 4 zones fixes en coordonnées écran (`self.surface`) :**
- Top-left : label "1UP" clignotant + score courant.
- Top-center : label "HIGH SCORE" + top score (injecté depuis `App` via `Renderer.__init__(highscore: int)`).
- Top-right : label "LEVEL" + `current_level_index + 1 / total`.
- Bottom-left : icônes Pac-Man (sprite bouche mi-ouverte × `game.lives`) ; si `lives >= 10`, un seul sprite + label `x{lives}`.
- Bottom-right : label "CHEAT MODE" + "ON"/"OFF" (paramètre `cheat: bool` de `_draw_hud`).
**Helpers ajoutés à `Renderer` :**
- `_draw_text(text, x, y, color, current_time, blink)` : render centré sur `(x, y)`, blink à 250ms si demandé.
- `_draw_life_sprite(life_sprite, line_height, offset)` : blit d'une icône de vie avec décalage horizontal.
**`PacmanSprite.life_sprite` :**
- Attribut ajouté dans `sprite.py`. Initialisé à `None` **avant** `super().__init__()` pour ne pas écraser le résultat de `_build_frames()`. Assigné dans `_build_frames()` : frame index `[1]` de la variante `(Direction.LEFT, PacmanState.ALIVE)` (bouche mi-ouverte).
**`Renderer.__init__` :**
- `tile_size` désormais dynamique : `min(surface_width * 0.80 // (maze_width + 1), surface_height * 0.70 // (maze_height + 1))`. Élimine le downscale massif pour les grands mazes (ex. height=100) et garantit marges proportionnelles fixes.
- `maze_offset = tile_size // 2` (cohérent avec tile_size dynamique).
- `logical_surface` dimensionnée en `(maze_width + 1) * tile_size × (maze_height + 1) * tile_size`.
- `scale = 1` implicite — blit direct sans `transform.scale`.
- `surface.fill(Color.BLACK)` ajouté en tête de `draw()` pour nettoyer les marges entre frames (évite l'empilement du HUD).
**`_update_window` :**
- Aligne sur la même logique que `__init__` : recalcule `tile_size`, `maze_offset`, `logical_surface`, `scaled_w/h`, `offset_x/y`, et réinstancie les sprites (tile_size change entre niveaux).
**`Engine` :**
- Score plafonné à 3 333 360 (maximum de l'arcade original) : `self.score = min(self.score + points, 3333360)`.
**`App` :**
- Guard `if not self.running: break` après `_handle_transitions()` — évite le flash d'un frame parasite au quit depuis `EndScreen`.
- `highscore` injecté dans `Renderer.__init__` depuis `self.highscore.scores[0]["score"]` si scores non vide, sinon `0`.
**§3.5 HUD partiellement soldé :** score ✓, vies ✓, indicateur cheat ✓, niveau ✓. Restent ouverts : compte à rebours `level_max_time`, indicateur Frightened.

### #23 — 2026-09-01 — Timer de niveau

Ajout du timer de niveau dans `engine.py` et affichage dans le HUD.
**`Engine` :**
- `level_start_time: int = 0` — timestamp du démarrage effectif du niveau (après countdown).
- `time_remaining: int = self.config.level_max_time` — temps restant en secondes, mis à jour à chaque frame dans `update()`.
- `update()` : `level_start_time` setté quand `counting_down` passe à `False`. `time_remaining` calculé hors des blocs `counting_down` et `dying` : `max(0, level_max_time - (current_time - level_start_time) // 1000)`.
- `_next_level()` et `_reset_positions()` : `level_start_time = 0` et `time_remaining = config.level_max_time` pour reset propre entre niveaux et après mort.
**`Renderer._draw_hud` :**
- CHEAT MODE retiré du HUD.
- Top-right : "TIME" + `game.time_remaining`.
- Bottom-right : "LEVEL" + `game.current_level_index + 1 / total`.
**§3.5 HUD** : score ✓, vies ✓, niveau ✓, timer ✓, indicateur cheat retiré. Reste ouvert : indicateur Frightened.

### #24 — 2026-09-01 — Fix pause pendant countdown + timeout de niveau + ralentissement
**Fix `on_resume` — timestamps non décalés (3 cas)**
`engine.py` — `on_resume()` ne décalait pas trois timestamps par la durée de pause, les rendant inexacts à la reprise :
- `_countdown_start` : le temps de pause comptait comme du countdown écoulé → sortie immédiate de `counting_down` si la pause durait plus longtemps que le countdown restant.
- `_death_start` : idem pour l'animation de mort → skip de l'animation.
- `level_start_time` : le timer de niveau continuait de décompter pendant la pause.
Fix : `self._countdown_start += duration`, `self._death_start += duration`, `self.level_start_time += duration` ajoutés dans `on_resume()`.
**Timeout de niveau → vie perdue**
`engine.py` — `update()` : si `time_remaining == 0`, appel de `_player_hit()` immédiatement après le calcul de `time_remaining`.
**Ralentissement du gameplay (+15 % uniforme)**
Toutes les constantes de délai augmentées de ~15 % pour ralentir le gameplay sans altérer les ratios de vitesse relative :
- `_PLAYER_UPDATE_DELAY` : `[150, 133, 120, 120]` → `[175, 155, 140, 140]`
- Ghost SCATTER/CHASE : `[200, 175, 160, 160]` → `[235, 205, 190, 190]`
- Ghost FRIGHTENED : `[300, 275, 250, 250]` → `[350, 320, 295, 295]`
- Ghost RESPAWN : `[80, 80, 80, 80]` → `[95, 95, 95, 95]`

### #25 — 2026-09-03 — Cheat menu

**`src/game/cheat.py` — nouvelle classe `Cheat` :**
Dataclass simple avec 9 attributs : `invincibility`, `ghost_freeze`, `speed_boost`, `infinite_time`, `infinite_lives` (bools) ; `add_lives: int = 0` ; `lvl_skip`, `instant_win`, `instant_lose` (bools). Passée par référence à `Engine` et aux écrans cheat — un seul objet en mémoire, modifications immédiatement visibles dans `Engine`.
**`src/ui/screens/cheat_screen.py` — `CheatScreen` et `PauseCheatScreen` :**
`CheatScreen(Screen)` : menu de 5 toggles (Invincibility / Ghost Freeze / Speed Boost / Infinite Time / Infinite Lives). Layout 2 colonnes : labels `midleft` via `_draw_menu`, colonne droite ON/OFF dessinée manuellement via `getattr(self.cheat, attr)`. ENTER toggle via `setattr`. ESC → TITLE.
`PauseCheatScreen(CheatScreen)` : hérite de `CheatScreen`, étend `menu_items`/`cheat_attrs` avec 4 items supplémentaires (Add Life / Level Skip / Instant Win / Instant Lose). Overlay semi-transparent sur `frozen_frame`. `lives_menu = [1, 3, 5, 10]` + `lives_index` — LEFT/RIGHT cyclent la valeur sur l'item Add Life, colonne droite affiche la valeur numérique au lieu de ON/OFF. ENTER sur Add Life : `self.cheat.add_lives = lives_menu[lives_index]` + `next_screen = RESUME`. ENTER sur Level Skip : `cheat.lvl_skip = True` + `next_screen = GAME`. ESC → PAUSE.
**`src/utils/screen_state.py` :**
Ajout de `PAUSECHEAT`.
**`engine.py` — intégration des flags cheat dans `update()` :**
- `infinite_lives` : `self.lives = 99` en tête de chaque frame.
- `add_lives` : `self.lives += self.cheat.add_lives` puis reset à 0 — consommé une seule fois.
- `speed_boost` : delay joueur `//= 2` localement, constante `_PLAYER_UPDATE_DELAY` intacte.
- `infinite_time` : `remaining` forcé à `config.level_max_time` avant le calcul de `time_remaining`.
- `ghost_freeze` : boucle ghosts et `_check_collision()` enveloppées dans `if not self.cheat.ghost_freeze`.
- `invincibility` : `_handle_collision` — si ghost non-FRIGHTENED et `cheat.invincibility`, ne pas appeler `_player_hit()`.
- **Bug fix** : `_check_collision()` était dans la boucle `for ghost in self.ghosts` → appelée 4× par frame → jusqu'à 4 appels à `_player_hit()` simultanés. Déplacée hors de la boucle.
**`app.py` — wiring :**
- `self.cheat = Cheat()` persistant entre les parties, passé à chaque `Engine` et aux deux écrans cheat.
- `screens` : ajout `ScreenState.PAUSECHEAT: PauseCheatScreen(...)`.
- `_update` : `frozen_frame` blit si `PAUSE or PAUSECHEAT`.
- `_handle_transitions` :
  - `PAUSE` : `frozen_frame` et `on_pause()` capturés uniquement si la source est `GAME` (évite l'écrasement du frozen_frame au retour de PAUSECHEAT).
  - `GAME` : si `cheat.lvl_skip` → `engine._next_level()` sans recréer Engine (score et vies préservés), reset flag, `RESUME` non appelé (timestamps déjà réinitialisés par `_next_level`).
  - `RESUME` : `cheat.add_lives` consommé dans Engine, `on_resume()` appelé.
  - `END` : `instant_win` → `engine.victory = True` ; `instant_lose` → `engine.game_over = True` avant création de `EndScreen`.
**`end_screen.py` :**
`EndScreen.__init__` reçoit `score: int` en paramètre. `score_input` restructuré en 5 lignes (`"Your score:" / str(score) / "" / "Enter your name:" / username`). `draw()` met à jour `score_input[-1]` avec `self.username` à chaque frame.
**`screen.py` — `_draw_menu` :**
Paramètre `new_color: tuple | None` remplacé par `highlight: bool = True`. Si `True` : item à `menu_index` en rouge, reste en blanc. Si `False` : tout en blanc.
**Dead code identifié :**
`scaled = pygame.transform.scale(...)` dans `Renderer.draw()` : `scaled_w/h` sont identiques aux dimensions de `logical_surface` (tile_size calculé pour remplir l'écran), le transform est un no-op. Confirmé dead code — à retirer.


### #26 — 2026-09-03 — STOP AVEC CES SIGNALEMENTS DE MERDE
 
**Clarification — faux positifs récurrents à ne plus signaler :**
- `engine.py` — `_can_move()` : retour implicite `None` — NOT a bug. L'enum `Direction` couvre exhaustivement les 4 cas, la branche unreachable n'existe pas en pratique.
- `ghost.py` — `_choose_direction()` et `_target_position()` : `match` sans default case — NOT a bug. Même raison : enum exhaustif.


### #27 — 2026-09-03 — Bugfixes post-checkup

**`cheat_screen.py` — `PauseCheatScreen.handle_event` :**
K_LEFT et K_RIGHT distingués — LEFT décrémente `lives_index`, RIGHT incrémente.
**`app.py` — lvl_skip countdown :**
Suppression de `self.engine.on_resume(current_time)` après `engine._next_level()` dans le bloc `cheat.lvl_skip`. `_next_level()` resets déjà `_countdown_start` ; `on_resume()` le décalait dans le futur → countdown > 3s.
**`title_screen.py` :**
K_q ajouté → `next_screen = ScreenState.QUIT`.
**`game_screen.py` :**
K_p ajouté → `next_screen = ScreenState.PAUSE` (conformément au MONITORING §3.3).
**`renderer.py` — `_update_window()` :**
Ajout de `self.superpacgum_sprite = SuperPacgumSprite(self.tile_size)` au même endroit que la réinstanciation de `pacman_sprite` et `ghost_sprites`. Corrige le désalignement des super-pacgums lors du changement de taille de maze entre niveaux.

### #28 — 2026-09-03 — Bugfixes post code review #2

**`ghost.py` — `_choose_target_direction` : Manhattan conservé intentionnellement.**
Distance euclidienne (`math.hypot`) provoquait un bug où les fantômes tournent indéfiniment en rond dans certaines configurations de maze. Manhattan réduit massivement ce comportement. Arbitrage délibéré entre fidélité arcade et jouabilité sur maze généré procéduralement. Ligne `math.hypot` retirée.
**`renderer.py` — `_draw_countdown` : surface SRCALPHA déplacée dans `__init__`.**
Surface overlay recréée et reremplie à chaque frame — même pattern que le pause overlay corrigé en #16. Fix : `self.overlay` instancié une fois dans `__init__` (`pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)`, fill `(0, 0, 0, 150)`), réutilisé dans `_draw_countdown` par un simple `blit`. Dimensions fixes pour toute la session, pas de recréation dans `_update_window`.
**`renderer.py` — dead code retiré.**
Bloc `pygame.transform.scale` commenté (lignes 83–85), confirmé dead code en #25 — retiré. Condition `if self.pacman_sprite.life is not None` toujours vraie (`life` assigné inconditionnellement dans `PacmanSprite.__init__` après `super()`) — retirée.
**`app.py` — `self.renderer` potentiellement non défini.**
`self.renderer = Renderer(...)` était à l'intérieur du bloc `isinstance(highscore, int)` — si la condition était fausse, `self.renderer` n'existait jamais → `AttributeError` au premier accès. La condition est nécessaire pour Pyright (le type de `scores[0]['score']` est `str | int`). Fix : narrowing séparé de la construction — `highscore: int = 0`, narrowing via `isinstance`, puis `self.renderer` créé inconditionnellement après. Même correction dans `_handle_transitions / GAME`.
**`renderer.py` — `_draw_hud` : dimensions `transform.scale` typées en `int`.**
`self.font_size * 2.2` produisait un `float`. Wrappé en `int(...)` pour satisfaire Pyright.
**`engine.py` — constantes de délai désynchronisées avec le MONITORING.**
Tuning effectué après #24 non loggué. Valeurs réelles :
- `_PLAYER_UPDATE_DELAY` : `[195, 170, 155, 155]`
- Ghost SCATTER/CHASE : `[260, 225, 210, 210]`
- Ghost FRIGHTENED : `[385, 350, 325, 325]`
- Ghost RESPAWN : `[105, 105, 105, 105]`
**`end_screen.py` / `models_ui.py` — espaces autorisés dans les usernames.**
`EndScreen.handle_event` : filtre d'input `event.unicode.isalnum()` → `event.unicode.isalnum() or event.unicode == " "`. `PlayerScore._validate_username` : `username.isalnum()` → `all(c.isalnum() or c == " " for c in username)`. Conforme au MONITORING §3.2 "alphanumérique + espaces".
**`cheat_screen.py` — `PauseCheatScreen` : absence de colonne droite sur items 6–8 — comportement voulu.**
Level Skip, Instant Win, Instant Lose sont des actions ponctuelles, pas des toggles. Pas de statut ON/OFF à afficher. Cohérent avec d'autres menus du projet.

### #29 — 2026-09-04 — Bugfixes post code review #3
 
**`sprite.py` — `Sprite.update()` : `last_anim_update` réinitialisé au changement de variant.**
`last_anim_update` n'était pas remis à `current_time` lors d'un changement de variant. Si `current_time - last_anim_update >= anim_speed` au moment du changement (typiquement après une pause prolongée), `anim_tick` avançait à 1 dès le premier `update()` call → frame 0 du nouveau variant sautée. Cas critique : animation one-shot `DYING` tronquée après reprise de pause. Fix : `self.last_anim_update = current_time` ajouté dans le bloc `if variant != self._last_variant`.
**`engine.py` — `Engine.update()` : `ghost.update_delay` capturé avant `ghost.update()`.**
`update_delay` était assigné après `ghost.update()`, qui peut transiter `ghost.state` de FRIGHTENED vers SCATTER/CHASE. L'interpolation utilisait alors le delay du nouvel état (260ms) pour un mouvement effectué à l'ancien delay (385ms) → alpha = 1.0 atteint prématurément → glitch visuel sur la frame de transition. Fix : `old_delay = _GHOST_UPDATE_DELAY[ghost.state][lvl_idx]` capturé avant l'appel, réutilisé dans la condition et assigné à `ghost.update_delay` après.
**`engine.py` — `Engine.update()` : `add_lives` capé à 99 via `min()`.**
`add_lives` était appliqué après `self.lives = 99` (infinite_lives) → `lives` pouvait dépasser 99 pour 1 frame. Fix : `self.lives = min(self.lives + self.cheat.add_lives, 99)`. Si `infinite_lives` est on, `min(99 + N, 99) = 99` — `add_lives` est consommé sans dépassement.
**`renderer.py` — `_draw_hud()` : affichage "∞" si `infinite_lives`.**
Branchement sur `game.cheat.infinite_lives` pour afficher "∞" à la place des icônes de vie. `Engine.lives` reste `int` à 99.
**`highscore_screen.py` — `colors[i]` sans garde : non corrigé intentionnellement.**
`Highscore.add_score()` garantit le top 10 — `len(scores) > 10` est impossible. Guard non ajouté : masquerait un bug dans `Highscore` au lieu de crasher clairement.
 
### #30 — 2026-09-04 — Bugfixes post code review #4 + décision projet

**`end_screen.py` — `update()` : `logo_alpha` hors bornes corrigé.**
Pour `elapsed` ∈ [2500, 3500ms], `fade_out_progress = min(1.0, (elapsed - 3500) / 800)` produisait une valeur négative → `logo_alpha` dépassait 255. Pygame clampait silencieusement, pas de bug visuel, mais valeur stockée incorrecte. Fix : `min(1.0, max(0.0, (elapsed - 3500) / 800))`.
**`renderer.py` — `_draw_hud` : décalage "xinf" — comportement voulu.**
Le `+ line_height // 2` supplémentaire dans la branche `infinite_lives` est intentionnel : "xinf" compte 4 caractères contre 2–3 pour "x{N}", le léger décalage compense visuellement.
**Bonus retirés du scope.**
L'intégralité des bonus (son, multijoueur réseau local, reskins, Blinky Cruise Elroy, tunnel wraparound) est abandonnée. Le programme est fonctionnel et stable — investir du temps sur des bonus non requis n'est pas justifié à ce stade.
