# Pac-Man — Suivi de Projet

## Architecture de référence

```
pac-man.py                  → point d'entrée, boucle principale
src/config/
    __init__.py
    loader.py               → chargement et validation du JSON
    models_config.py        → Config, LevelConfig
src/game/
    __init__.py
    game.py                 → logique principale, update loop
    player.py               → Player (position, direction)
    ghost.py                → Ghost (IA, déplacement)
    ghost_type.py           → enum GhostType (BLINKY/PINKY/INKY/CLYDE)
    ghost_state.py          → enum GhostState (CHASE/SCATTER/FRIGHTENED/RESPAWN)
    level.py                → Level (maze + placement pacgums/super/ghosts)
    direction.py            → enum Direction
    cell_content.py         → enum CellContent
src/maze/
    __init__.py
    adapter.py              → conversion maze externe → modèles internes
    generator.py            → MazeFactory (wrapper du module externe)
    models_maze.py          → Maze, Cell
src/renderer/
    __init__.py
    renderer.py             → Renderer (pygame)
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
- [ ] `game.py` : tracker le temps écoulé depuis le début du niveau.
- [ ] Déclencher une mort du joueur si `level_max_time` (secondes) est atteint — une vie perdue, positions réinitialisées.
- [ ] Afficher le compte à rebours dans le HUD.

### 3.2 Highscore — système persistant
- [ ] Créer `src/highscore/` (manager + modèle).
- [ ] Charger au démarrage depuis `config.highscore_filename`.
- [ ] Sauvegarder après chaque fin de partie (game over ou victoire).
- [ ] Valider les noms : max 10 caractères, alphanumérique + espaces.
- [ ] Conserver le **top 10** des scores, triés par ordre décroissant.
- [ ] Robuste aux erreurs : fichier absent, JSON invalide, permissions.

### 3.3 Écrans de menu

#### Title Screen
- [ ] **Logo** : "PAC-MAN" style original (logo pixel-art statique).
- [ ] **Animation** : une ligne sous le logo — les 4 fantômes poursuivent Pac-Man de droite à gauche → Pac-Man mange un super-pacgum → se retourne → mange les fantômes un par un (séquence en boucle).
- [ ] **Menu** en dessous de l'animation :
  - **Play**
  - **Highscores**
  - **Cheat Mode** (accès à la configuration des cheats)
  - **Quit**
- [ ] Navigation clavier (flèches + Entrée).

#### End Screen (Game Over / Victory)
- [ ] Même écran, message différent : **"GAME OVER"** (vies épuisées) vs **"YOU WIN"** (tous niveaux complétés).
- [ ] Afficher le score final.
- [ ] Saisie du nom du joueur (max 10 chars, filtrage des caractères invalides).
- [ ] Options post-saisie : **Rejouer** / **Menu principal** / **Quitter**.

#### Highscore Screen
- [ ] Afficher le top 10 (rang + nom + score).
- [ ] Accessible depuis le title screen.
- [ ] Mettre en évidence le score qui vient d'être enregistré.

#### Pause Menu
- [ ] Déclenché par `ESC` ou `P` pendant le jeu.
- [ ] Jeu entièrement gelé (timer, ghosts, player).
- [ ] Options : **Reprendre** / **Cheat Mode** / **Menu principal** / **Quitter**.

### 3.4 Cheat Mode
Configurable depuis le **Title Screen** et depuis le **Pause Menu**. Chaque option est un toggle ou une action :

- [ ] **Invincibility** : toggle — collisions avec ghosts non-frightened désactivées.
- [ ] **Level Skip** : action — passe immédiatement au niveau suivant.
- [ ] **Ghost Freeze** : toggle — les ghosts ne se déplacent plus.
- [ ] **Extra Life** : action — ajoute +X vies (valeur X à définir, ex. +1 ou +3).
- [ ] **Increased Speed** : toggle — ajoute +X% à la vitesse de Pac-Man (valeur X à définir).
- [ ] Interface cheat : écran dédié avec la liste des cheats, état actif/inactif visible, navigable au clavier.
- [ ] Indicateur visuel discret en HUD quand au moins un cheat est actif (ex. "CHEAT" en coin).

### 3.5 HUD en jeu (refonte renderer)
- [ ] Score.
- [ ] Vies (icônes Pac-Man miniatures ou chiffre).
- [ ] Compte à rebours `level_max_time`.
- [ ] Numéro de niveau en cours.
- [ ] Indicateur Frightened (effet visuel global ou texte discret).
- [ ] Indicateur cheat actif.

### 3.6 Graphisme arcade 1980

#### Pac-Man
- [ ] Cercle jaune avec **bouche animée** (arc qui s'ouvre/ferme selon la direction de déplacement).
- [ ] Orientation de la bouche selon `player.direction`.
- [ ] Animation de mort (séquence : bouche qui s'ouvre à 360° puis disparaît).
- [ ] Séquence "READY!" au démarrage de chaque niveau (texte clignotant, brève pause avant de jouer).

#### Fantômes
- [ ] Sprite fantôme classique : corps arrondi, bas dentelé, **yeux directionnels**.
- [ ] Frightened : corps bleu uni.
- [ ] Frightened clignotant (bleu/blanc, dernières ~2s — lié à § 2.6).
- [ ] Respawn : **yeux seuls** se déplaçant vers le spawn.
- [ ] Couleurs par type : Blinky rouge, Pinky rose, Inky cyan, Clyde orange.

#### Maze & élémentsBrother DCP-L2627DWE
- [ ] Murs style bleu néon (coins arrondis si possible).
- [ ] Pacgums : petits points blancs centrés.
- [ ] Super-pacgums : gros points blancs **clignotants**.
- [ ] Fond noir.

#### UI & typographie
- [ ] Police arcade (ex. Press Start 2P ou équivalent libre).
- [ ] Disposition HUD cohérente avec le style visuel général.

---

## 4. Bonus (si temps disponible)

### 4.1 Son
- [ ] Musique de fond (thème arcade).
- [ ] Bruitages : manger pacgum, manger super-pacgum, manger fantôme, mort, niveau suivant, victoire.
- [ ] Contrôle volume / mute.
Brother DCP-L2627DWE
### 4.2 Tunnel wraparound
- [ ] `game.py` — `move_player()` : si le joueur sort par le bord gauche/droit, téléporter au bord opposé.
- [ ] Même logique pour `ghost.py` — `_move()`.
- [ ] Vérifier la compatibilité avec la structure des bords des mazes générées aléatoirement.

### 4.3 Multijoueur réseau local
Architecture : **client/serveur TCP**. Un joueur héberge (serveur, IP locale type `192.168.x.x` + port), les autres se connectent en entrant cette adresse.

- [ ] Module réseau à créer (`src/network/`).
- [ ] 1 Pac-Man obligatoire (hôte ou client), jusqu'à 4 joueurs supplémentaires incarnant des fantômes.
- [ ] Écran de lobby : hôte crée la partie (affiche son IP/port), clients entrent l'adresse.
- [ ] Synchronisation d'état : positions, score, vies, état des ghosts, pacgums mangés.
- [ ] Gestion des déconnexions (joueur fantôme qui quitte → ghost repasse en IA).

### 4.4 Reskin de sprites
- [ ] Pac-Woman (sprite alternatif).
- [ ] Sélection de skin depuis le menu principal.
- [ ] (Optionnel) Mode graphique "moderne" vs "arcade 1980".

### 4.5 Blinky "Cruise Elroy"
- [ ] Quand le nombre de pacgums restants passe sous un seuil, Blinky ignore le Scatter et accélère.Brother DCP-L2627DWE

---

## État des lieux

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
