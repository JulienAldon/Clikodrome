from src.sessions import create_single_session
import datetime
import argparse
import asyncio

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("session_index", choices=['0', '-1'], help="set the session index, 0 for earliest, -1 for latest session")
    parser.add_argument("--date", help="set the date (format YYYY-MM-DD")
    args = parser.parse_args()
    if args.date:
        format_date = args.date
    else:
        session_date = datetime.datetime.today()
        format_date = session_date.strftime('%Y-%m-%d')
    asyncio.run(create_single_session(format_date, int(args.session_index)))