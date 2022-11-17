from src.sessions import sign_all_sessions
import datetime
import argparse
import asyncio

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("session_index", choices=['0', '-1'], help="set the session index, 0 for earliest session, -1 for latest session")
    parser.add_argument("--date", help="set the date (format YYYY-MM-DD)")
    args = parser.parse_args()
    if args.date:
        current_date = args.date
    else:
        current_date = datetime.datetime.today().strftime('%Y-%m-%d')[:10]
    session_index = args.session_index
    asyncio.run(sign_all_sessions(current_date, int(session_index)))