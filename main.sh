echo "Scrapping Resident Advisor..."
./Scrapping/ResidentAdvisor/run.sh
echo "[DONE] Scrapping Resident Advisor"

echo "Scrapping Events.Ch..."
python ./Scrapping/events.ch/run.py
echo "[DONE] Scrapping Events.Ch..."

echo "Scrapping Route des Festivals..."
./Scrapping/RouteDesFestivals/run.sh
echo "[DONE] Scrapping Route des Festivals..."


echo "Merging + Augmenting Dataframes"
python ./Scrapping/mergeDataframes.py
echo "[DONE] Merging + Augmenting Dataframes"
