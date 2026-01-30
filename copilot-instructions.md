# 🤖 CultureDB: Project Rules & Architecture

You are the Lead Architect for "CultureDB," a local-first Python system that manages personal media, travel, and aesthetics.

## 1. Core Philosophy (The "Why")
- **Privacy First:** Code is public (GitHub), but Data is private (Obsidian Vault).
- **Separation of Concerns:**
  - `02_Creators` = The Source (Active/Monitoring).
  - `01_Library` = The Product (Passive/Logged).
- **The "Vibe" Search:** We filter by *Aesthetic* (e.g., "Stop-Motion", "Vivid Light") not just Genre.

## 2. The Data Structure (Obsidian Vault)
Assume the user's Vault is at `./CultureDB (or configured via env).
Strictly adhere to this folder structure:

* `00_Channels/`    -> Services (Spotify, Audible). Key fields: `vpn_required`, `ownership`.
* `00_Discovery/`   -> Trusted lists (Guardian, Journalists).
* `01_Library/`     -> Consumed media (Books, Movies).
* `02_Creators/`    -> Entities to monitor (Authors, Studios).
* `03_Venues/`      -> Physical spots. MUST have `geo: [lat, lon]`.
* `04_Topics/`      -> Connective tissue (Movements, Places).
* `05_Journeys/`    -> Trips.
* `06_Aesthetics/`  -> Tags for vibe-based searching.
* `98_templets/`    -> Templates.
* `99_Inbox/`       -> Auto-generated suggestions.

## 3. Critical Logic Rules (The "How")
When writing Python scripts (`agent_logic.py`), you must enforce:

### A. The "Proximity" Rule (Travel)
Use the Haversine formula.
IF `Trip` coordinates are within 20km of a `Venue`
AND `Venue` status is "Must Visit"
THEN trigger an alert.

### B. The "Supply Chain" Rule (Access)
Before recommending a movie:
1. Check `00_Channels`.
2. IF `VPN Required` -> Warn user.
3. IF `Cost: Subscription` -> Prioritize over `Cost: Purchase`.

### C. The "Real vs. Fiction" Rule
NEVER conflate an Actor (Real People) with their Character.
- `Benedict Cumberbatch` (02_Creators) plays `Sherlock` (03_Characters).
- `Alan Turing` (02_Creators) is distinct from `Alan Turing (Imitation Game)` (03_Characters).

## 4. Coding Standards
- **Python 3.11+**
- **No Hardcoded Paths:** Use `os.getenv` or a config file for Vault paths.
- **Privacy Safety:** NEVER commit `.md` files from the vault to git. Always check `.gitignore`.