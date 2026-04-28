import json
import pytest
from pathlib import Path
from app.services import hydrator

def test_upgrade_songs():
    # 1. Setup local 'stash' paths
    current_dir = Path(__file__).parent
    stash_dir = current_dir / "stash"
    stash_dir.mkdir(exist_ok=True)
    
    input_path = stash_dir / "starting_pack.json"
    output_path = stash_dir / "upgraded_pack.json"

    # 2. Check for the stash file
    if not input_path.exists():
        pytest.fail(f"📂 STASH MISSING: Put your JSON file here: {input_path}")

    # 3. Load the data
    with open(input_path, "r") as f:
        raw_data = json.load(f)

    print(f"\n📂 Loaded {len(raw_data)} tracks for metadata upgrade.")

    # 4. Run the 'Upgrade' logic (Apple lookup only, no Spotify)
    try:
        # Check if "songs" is the right key in your JSON
        # If your JSON uses "tracks", change "songs" to "tracks" below
        songs_to_upgrade = raw_data.get("songs", [])
        
        if not songs_to_upgrade:
            pytest.fail("❌ No songs found in the 'songs' key of your JSON!")

        upgraded_list = hydrator.upgrade_existing_songs(songs_to_upgrade)
        
        # 5. Serialize back to JSON
        output_data = [s.model_dump() for s in upgraded_list]
        
        # Optional: If you want to keep the session wrapper in the output:
        # raw_data["songs"] = output_data
        # json.dump(raw_data, f, indent=2)

        with open(output_path, "w") as f:
            json.dump(output_data, f, indent=2)

        print(f"✅ Success! Metadata upgraded for {len(output_data)} tracks.")
        
    except Exception as e:
        pytest.fail(f"💥 Upgrade failed: {e}")