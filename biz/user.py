from models.core import User, GameBoard, mysql_db


if __name__ == "__main__":
    User.init_user("admin", "admin")
    User.init_user("user", "user")
    # print(get_user_by_username("admin"))
    # print(get_user_by_username("user"))
    # print(get_user_by_username())
    user = User.get_user_by_username("user")
    admin = User.get_user_by_username("admin")
    game = GameBoard.create_game("test", admin._id)
    game.user_join_game(user._id, 200)
    game.user_join_game(admin._id, 200)

    game.balance_trancefer(user._id, admin._id, 100)
    print(game)