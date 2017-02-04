echo "Scrapping Resident Advisor..."
./Scrapping/ResidentAdvisor/run.sh
echo "[DONE] Scrapping Resident Advisor"

read -rsp $'Press any key to continue...\n' -n 1 key

echo "Scrapping Events.Ch..."
python ./Scrapping/events.ch/run.py
echo "[DONE] Scrapping Events.Ch..."

read -rsp $'Press any key to continue...\n' -n 1 key

echo "Scrapping Route des Festivals..."
./Scrapping/RouteDesFestivals/run.sh
echo "[DONE] Scrapping Route des Festivals..."

read -rsp $'Press any key to continue...\n' -n 1 key

echo "Merging + Augmenting Dataframes"
python ./Scrapping/mergeDataframes.py
echo "[DONE] Merging + Augmenting Dataframes"

read -rsp $'Press any key to continue...\n' -n 1 key

echo "Extracting genres in Dataframes"
python ./Scrapping/ArtistsPipeline.py
echo "[DONE] Extracting genres in Dataframes"