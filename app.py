import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

# Load Q-table
with open("q_table.pkl", "rb") as f:
    q_table = pickle.load(f)

# App config
st.set_page_config(page_title="🏏 Cricket Match Simulator", layout="wide")
st.title("🏏 Cricket Match Tracker")

# Sidebar: Match Settings
st.sidebar.header("🔧 Match Settings")
match_type = st.sidebar.radio("Select Match Format:", ["10 Overs", "20 Overs (T20)", "50 Overs (ODI)"])
match_overs = {"10 Overs": 10, "20 Overs (T20)": 20, "50 Overs (ODI)": 50}
total_overs = match_overs[match_type]

# Sidebar: Match Conditions
st.sidebar.markdown("🎯 **Player Skill Factor (Higher = Better)**")
extra_run_chance = st.sidebar.slider("✨ Chance of Extra Run", 0.00, 0.10, 0.03, 0.01)
wicket_modifier = st.sidebar.slider("☠️ Wicket Base Modifier", 0.00, 0.20, 0.05, 0.01)

# Sidebar: Team Names
team_a = st.sidebar.text_input("🏏 Team A (Batting First):", value="Team Alpha")
team_b = st.sidebar.text_input("🏏 Team B (Chasing):", value="Team Bravo")

# Sidebar: Team A Players & Skills
st.sidebar.subheader(f"👥 {team_a} Lineup and Batting Skills")
team_a_players, team_a_batting_skills, team_a_bowling_skills = [], [], []
for i in range(1, 12):
    name = st.sidebar.text_input(f"{team_a} Player {i} Name", value=f"{team_a} P{i}")
    bat_skill = st.sidebar.slider(f"{name} Batting Skill", 0.0, 1.0, 0.5, key=f"{name}_bat")
    bowl_skill = st.sidebar.slider(f"{name} Bowling Skill", 0.0, 1.0, 0.5, key=f"{name}_bowl")
    team_a_players.append(name)
    team_a_batting_skills.append(bat_skill)
    team_a_bowling_skills.append(bowl_skill)

# Sidebar: Team B Players & Skills
st.sidebar.subheader(f"👥 {team_b} Lineup and Batting Skills")
team_b_players, team_b_batting_skills, team_b_bowling_skills = [], [], []
for i in range(1, 12):
    name = st.sidebar.text_input(f"{team_b} Player {i} Name", value=f"{team_b} P{i}")
    bat_skill = st.sidebar.slider(f"{name} Batting Skill", 0.0, 1.0, 0.5, key=f"{name}_bat")
    bowl_skill = st.sidebar.slider(f"{name} Bowling Skill", 0.0, 1.0, 0.5, key=f"{name}_bowl")
    team_b_players.append(name)
    team_b_batting_skills.append(bat_skill)
    team_b_bowling_skills.append(bowl_skill)

def simulate_innings(team_name, players, bat_skills, overs, bowling_team=None, bowling_skills=None):
    st.subheader(f"🏁 {team_name} Innings")

    total_balls = overs * 6
    balls_left = total_balls
    decisions, cumulative_runs = [], []
    wickets = 0
    max_wickets = 10
    total_runs, player_score, player_number = 0, 0, 0
    scorecard = {}
    wickets_info = {}  # bowler_name -> wickets taken
    balls_bowled = {}  # bowler_name -> balls bowled

    target_score = None
    if bowling_team:
        target_score = bowling_team.get("target")
        bowlers = bowling_team["players"][-5:]
        bowler_skills = bowling_team["skills"][-5:]
    else:
        bowlers = []
        bowler_skills = []

    # Allowed actions only: no 5 runs
    actions_map = {
        0: ("Defend", 0),
        1: ("Single", 1),
        2: ("Double", 2),
        3: ("Boundary (4)", 4),
        4: ("Six", 6)
    }

    runs_to_action = {
        0: "Defend",
        1: "Single",
        2: "Double",
        3: "Triple",
        4: "Boundary (4)",
        6: "Six"
    }

    # Assign bowlers in rotation (simplified)
    current_bowler_index = 0
    balls_bowled_per_bowler = {bowler: 0 for bowler in bowlers}

    while balls_left > 0 and wickets < max_wickets and (not target_score or total_runs < target_score):
        over_number = (total_balls - balls_left) // 6 + 1
        ball_number = (total_balls - balls_left) % 6 + 1

        current_bowler = bowlers[current_bowler_index] if bowlers else "Random Bowler"

        # Increment balls bowled by current bowler
        balls_bowled_per_bowler[current_bowler] = balls_bowled_per_bowler.get(current_bowler, 0) + 1

        state = (
            min(balls_left, q_table.shape[0] - 1),
            min(999 if not target_score else target_score - total_runs, q_table.shape[1] - 1)
        )
        q_values = q_table[state[0], state[1]]
        valid_action_indices = list(actions_map.keys())
        q_values_filtered = {i: q_values[i] for i in valid_action_indices}
        action_index = max(q_values_filtered, key=q_values_filtered.get)

        original_action_name, original_runs = actions_map[action_index]

        skill_factor = bat_skills[player_number]
        final_runs = original_runs
        if random.random() > skill_factor:
            final_runs = max(0, original_runs - 1)

        is_out = False
        base_wicket_chance = 0.05 if original_action_name in ["Single", "Double", "Defend"] else 0.10
        if random.random() < base_wicket_chance * (1 - skill_factor + wicket_modifier):
            is_out = True
            final_runs = 0
            scorecard[players[player_number]] = player_score
            wickets_info[current_bowler] = wickets_info.get(current_bowler, 0) + 1

            decision = f"Over {over_number}.{ball_number} → Action: {runs_to_action.get(final_runs, 'Run(s)')}, Runs: {final_runs} ❌ {players[player_number]} is OUT! Bowler: {current_bowler}"

            player_number += 1
            player_score = 0
            wickets += 1

            # Change bowler every over
            if ball_number == 6:
                current_bowler_index = (current_bowler_index + 1) % len(bowlers)

        else:
            extra_run = 0
            if random.random() < extra_run_chance:
                extra_run = 1
                final_runs += extra_run
            decision = f"Over {over_number}.{ball_number} → Action: {runs_to_action.get(final_runs, 'Run(s)')}, Runs: {final_runs}"
            if extra_run:
                decision += " +1 extra"

            # Change bowler every over
            if ball_number == 6:
                current_bowler_index = (current_bowler_index + 1) % len(bowlers)

        total_runs += final_runs
        balls_left -= 1
        player_score += final_runs
        cumulative_runs.append(total_runs)
        decisions.append(decision)

        if player_number >= len(players):
            break

    if player_number < len(players) and not is_out:
        scorecard[players[player_number]] = player_score

    # Prepare bowling summary with overs bowled and wickets
    bowling_summary = {}
    for bowler, balls in balls_bowled_per_bowler.items():
        overs_bowled = balls // 6 + (balls % 6) / 6
        wickets_taken = wickets_info.get(bowler, 0)
        bowling_summary[bowler] = {"Overs": round(overs_bowled, 1), "Wickets": wickets_taken}

    # Display summary
    st.write(f"🏏 Team: {team_name}")
    st.write(f"🏆 Runs Scored: {total_runs}")
    st.write(f"💥 Wickets Lost: {wickets}")
    st.write(f"🕐 Balls Used: {total_balls - balls_left}")
    if target_score:
        st.write(f"🎯 Target Score: {target_score}")
        if total_runs >= target_score:
            st.success("🎉 Target Achieved! Victory!")
        elif wickets >= max_wickets:
            st.error("💔 All Out! Target Not Achieved.")
        else:
            st.error("⏳ Overs Finished! Target Not Achieved.")

    st.subheader("🧠 Ball-by-Ball Commentary")
    for d in decisions:
        st.write("📌", d)

    st.subheader("📈 Batting Scorecard")
    for player, runs in scorecard.items():
        st.write(f"{player}: {runs} runs")

    if bowling_summary:
        st.subheader("🎳 Bowling Summary")
        for bowler, stats in bowling_summary.items():
            st.write(f"{bowler}: {stats['Overs']} overs, {stats['Wickets']} wickets")

    return total_runs, decisions, cumulative_runs, target_score

# Run Simulation
if st.button("🚀 Simulate Match"):
    st.subheader("🔁 First Innings")
    team_a_score, a_decisions, a_cumulative, _ = simulate_innings(
        team_a, team_a_players, team_a_batting_skills, total_overs,
        bowling_team={"players": team_b_players, "skills": team_b_bowling_skills}
    )

    st.subheader("🔁 Second Innings (Chasing)")
    team_b_score, b_decisions, b_cumulative, _ = simulate_innings(
        team_b, team_b_players, team_b_batting_skills, total_overs,
        bowling_team={"players": team_a_players, "skills": team_a_bowling_skills, "target": team_a_score + 1}
    )

    # Result display
    st.header("🏆 Match Result")
    if team_a_score == team_b_score:
        st.info("🤝 Match Drawn / Tie!")
    elif team_b_score > team_a_score:
        st.success(f"💥 {team_b} wins!")
    else:
        st.error(f"💥 {team_a} wins!")

    # Plot score progression
    st.subheader("📊 Score Progression")
    overs_axis_a = np.arange(1, len(a_cumulative) + 1) / 6
    overs_axis_b = np.arange(1, len(b_cumulative) + 1) / 6
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=overs_axis_a, y=a_cumulative, label=team_a)
    sns.lineplot(x=overs_axis_b, y=b_cumulative, label=team_b)
    plt.xlabel("Overs")
    plt.ylabel("Runs")
    plt.title("Runs vs Overs")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
