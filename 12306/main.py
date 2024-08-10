from rich.console import Console

import env


class BuyTicket:

    def __init__(self, env_file):
        # self.driver = ChromiumPage()
        self.accounts = env_file
        self.console = Console()

    def read_env(self):
        for account in self.accounts:
            for station in account['station']:
                for date_range in account['date']:
                    for date in date_range:
                        for ticket_type in account['ticket_type']:
                            for train_type in account['train_type']:
                                for seat_type in account['seat_type']:
                                    for position in account['position']:
                                        # 使用ticket_provider进行查询
                                        self.query_ticket(account['username'], station[0], station[1], date, ticket_type, train_type, seat_type, position)
                                        # 只需在此处添加break，确保只使用每个日期进行一次查询
                                        break

    def query_ticket(self, username, origin, destination, date, ticket_type, train_type, seat_type, position):
        # 实际的查询逻辑
        self.console.print(f"用户：{username}，始发地：{origin}，目的地：{destination}，日期：{date}，票种：{ticket_type}，列车类型：{train_type}，座位类型：{seat_type}，座位位置：{position}")


if __name__ == "__main__":
    ticket_provider = BuyTicket(env.ACCOUNTS)
    ticket_provider.read_env()
