import argparse
from .loader import load_competitions_from_csv, load_profile_from_json
from .scoring import recommend

def main():
    p = argparse.ArgumentParser(description="CompMatch MVP CLI")
    p.add_argument("--profile", required=True, help="path to student_profile.json")
    p.add_argument("--data", required=True, help="path to competitions_seed.csv")
    p.add_argument("--topk", type=int, default=8, help="how many recommendations to show")
    args = p.parse_args()

    profile = load_profile_from_json(args.profile)
    competitions = load_competitions_from_csv(args.data)
    recs = recommend(profile, competitions, topk=args.topk)

    print(f"\n✅ 推荐结果 Top {len(recs)}（grade={profile.grade}, tier={profile.target_tier}, weekly_hours={profile.weekly_hours}h）\n")
    for i, r in enumerate(recs, start=1):
        c = r.competition
        print(f"{i}. {c.name} | subject={c.subject} | diff={c.difficulty}/5 | roi={c.roi}/5 | prestige={c.prestige}/5 | score={r.score:.1f}")
        print("   why:", "；".join(r.reasons[:3]))
        if r.warnings:
            print("   ⚠️ ", "；".join(r.warnings[:2]))
        if c.link:
            print("   link:", c.link)
        print()

if __name__ == "__main__":
    main()
