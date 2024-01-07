from pathlib import Path

from src.data.db_connection import DataConnection

from utils.loading_file import load_yaml
from utils.download import down_derivative_matched_db 

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]


def main():
    
    db_account = load_yaml(ROOT / "configs" / "usr" / "db_account.yaml")
    # Data query
    user, password, host, port, db_name =   db_account['user'],\
                                            db_account['pass'], \
                                            db_account['host'], \
                                            db_account['port'], \
                                            db_account['database']
    db_conn = DataConnection(user, password, host, port, db_name)
    down_derivative_matched_db(db_conn, 
                               '2023-09-15', 
                               '2023-09-15', 
                               '10:30:00', 
                               '11:29:45', 
                               10, 
                               'train.csv')
    
    down_derivative_matched_db(db_conn, 
                               '2023-09-15', 
                               '2023-09-15', 
                               '10:30:00', 
                               '11:29:45', 
                               10, 
                               'val.csv')


if __name__ == "__main__":
    main()
