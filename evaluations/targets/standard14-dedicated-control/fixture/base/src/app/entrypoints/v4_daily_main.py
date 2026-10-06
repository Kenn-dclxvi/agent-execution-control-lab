from src.app.v4_engine import V4PortfolioEngine
import argparse
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("date", nargs="?")
    args = parser.parse_args()
    engine = V4PortfolioEngine()
    engine.run(target_date=args.date)
if __name__ == "__main__":
    main()
