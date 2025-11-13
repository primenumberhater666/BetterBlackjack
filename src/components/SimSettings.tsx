
import { useState } from "react";
import '../App.css'
import NumberEntry from './NumberEntry';
import Button from 'react-bootstrap/Button';

function SimSettings() {
    const [numSims, setNumSims] = useState(1000000); // WARNING: 1 MILLION SIMS IS NOT NEARLY ENOUGH FOR AN ACCURATE RESULT. SIM 10 MILLION ROUNDS MINIMUM!!!   
    const [roundsPerHour, setRoundsPerHour] = useState(100); 
    const [bankroll, setBankroll] = useState(250000); 
    const [decks, setDecks] = useState(2);
    const [penetrationPct, setPenPct] = useState(0.75); 

    const [bets, setBets] = useState<number[]>(Array(10).fill(0));
    const setBet = (i: number, v: number) =>
      setBets((b) => b.map((x, idx) => (idx === i ? v : x)));
    const [players, setPlayers] = useState(1);
    const [twoHandsTc, setTwoHandsTc] = useState(999);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);

    // penetration given by user is % of decks dealt. We convert it to the number of cards
    // remaining before the shuffle. 
    const penetrationCards = Math.round(52 * decks * (1 - penetrationPct));

    const spread = [
        { count: -2, bet: bets[0] },
        { count: -1, bet: bets[1] },
        { count: 0, bet: bets[2] },
        { count: 1, bet: bets[3] },
        { count: 2, bet: bets[4] },
        { count: 3, bet: bets[5] },
        { count: 4, bet: bets[6] },
        { count: 5, bet: bets[7] },
        { count: 6, bet: bets[8] },
        { count: 7, bet: bets[9] },
    ];

    const startSim = async () => {
        setLoading(true);
        setError(null);
        setResult(null);
        try {
          const res = await fetch("/sim", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              num_sims: numSims,
              rounds_per_hour: roundsPerHour,
              starting_bankroll: bankroll,
              decks_used: decks,
              penetration_cards: penetrationCards,
              spread,
              players,                
              two_hands_tc: twoHandsTc, 
            }),
          });
          // ser
          if (!res.ok) throw new Error(`Server error ${res.status}`);
          const data = await res.json();
          setResult(data);
        } catch (e: any) {
          setError(e.message);
        } finally {
          setLoading(false);
        }
      };

    return (<> 

       <div className="sim col-1">
        <div className="settingItem">
          <p className="settings-text"> Betting </p>
        </div>
        <div className="settingEntry">
          <NumberEntry value={bets[0]} onChange={(v) => setBet(0, v)} />
        </div>
        <div className="settingEntry">
          <NumberEntry value={bets[1]} onChange={(v) => setBet(1, v)} />
        </div>
        <div className="settingEntry">
          <NumberEntry value={bets[2]} onChange={(v) => setBet(2, v)} />
        </div>
        <div className="settingEntry">
          <NumberEntry value={bets[3]} onChange={(v) => setBet(3, v)} />
        </div>
        <div className="settingEntry">
          <NumberEntry value={bets[4]} onChange={(v) => setBet(4, v)} />
        </div>
        <div className="settingEntry">
          <NumberEntry value={bets[5]} onChange={(v) => setBet(5, v)} />
        </div>
        <div className="settingEntry">
          <NumberEntry value={bets[6]} onChange={(v) => setBet(6, v)} />
        </div>
        <div className="settingEntry">
          <NumberEntry value={bets[7]} onChange={(v) => setBet(7, v)} />
        </div>
        <div className="settingEntry">
          <NumberEntry value={bets[8]} onChange={(v) => setBet(8, v)} />
        </div>
        <div className="settingEntry">
          <NumberEntry value={bets[9]} onChange={(v) => setBet(9, v)} />
        </div>
        
        </div>
        <div className = "sim col-1">
            <div className = "settingItem "> 
                <p className = "settings-text"> Bankroll </p>
                <NumberEntry value={bankroll} onChange={setBankroll}></NumberEntry>
            </div>
            <div class = "settingItem "> 
                <p class = "settings-text"> Rounds per Hour  </p>
                <NumberEntry value={100} onChange={setRoundsPerHour}></NumberEntry>
                </div>
            <div class = "settingItem "> 
                <p class = "settings-text"> Decks Used </p>
                <select className="form-select" value={decks} 
                    onChange = {(e) => 
                        setDecks(Number(e.target.value))}
                    class ="form-select" 
                    aria-label="Select Number of Decks">
                    <option selected ={2}>2 decks</option>
                    <option value={4}>4 decks</option>
                    <option value={6}>6 decks</option>
                    <option value={8}>8 decks</option>
                </select>
            </div>
            <div class = "settingItem "> 
                <p class = "settings-text"> Deck Penetration </p>
                    <select class="form-select" className="form-select" value={penetrationPct}
                    onChange = {(e) => 
                        setPenPct(Number(e.target.value))}
                    aria-label="Select Deck Penetration">
                        <option value={0.5}>50%</option>
                        <option value={0.6}>60%</option>
                        <option value={0.75}>75%</option>
                        <option selected={0.8}>80% </option>
                        <option value={0.85}>85% </option>
                        <option value={0.9}>90% </option>
                    </select>
                </div>
            <div class = "settingItem "> 
                <p class = "settings-text"> Number of Players </p>
                    <select class="form-select" className="form-select" value={players}
                    onChange = {(e) => 
                        setPlayers(Number(e.target.value))}
                    aria-label="Number of Players">
                        <option value={1}>1</option>
                        <option value={2}>2</option>
                        <option selected={3}>3 </option>
                        <option value={4}>4</option>
                        <option value={5}>5 </option>
                        <option value={6}>6 </option>
                        <option value={7}>7 </option>
                    </select>
                </div>

                <div className="settingItem">
                    <p className="settings-text"> Two Hands @ TC (set 999 to play one hand only)</p>

                    <NumberEntry value={twoHandsTc} onChange={setTwoHandsTc} />
                </div>

            <Button type="button" className = "btn" disabled = {loading} onClick = {startSim}> 
                {loading ? "Running Sims" : "Start Sim"}
            </Button>

            {result && (
                <div style={{ marginTop: 12 }}>
                <div>Hands played: {result.hands_played}</div>
                <div>Final bankroll: {result.final_bankroll}</div>
                <div>Profit: {result.profit}</div>
                <div>Profit / round: {result.profit_per_round}</div>
                <div>Profit / hour: {result.profit_per_hour}</div>
                <div>Std dev / hour: {result.stdev_per_hour}</div>
        </div>
      )}
       </div>
       </>
    );
}

export default SimSettings