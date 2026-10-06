from src.app.weekly_engine import WeeklyEngine
import argparse
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("date", nargs="?")
    args = parser.parse_args()
    engine = WeeklyEngine()
    engine.run(target_date=args.date)
if __name__ == "__main__":
    main()
