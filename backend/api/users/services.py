async def create_casual_user():
    """
        can create: admin
    """
    pass

async def create_editor():
    """
        can create: admin
    """
    pass

async def get_all_users():
    """
        maybe with articles or only users
    """
    pass

async def get_user_by_id(user_id: int):
    """
        can get: admin only
    """
    pass

async def update_user(): # will allow after permissions todo
    """
        can update: admin & account's owner
    """
    pass

async def delete_user():
    """
        can delete: admin
    """
    pass

async def block_user(user_id: int): # soft deletion
    """
        can block: admin only
        :param user_id:
        :return: blocked user
    """
    pass

async def unblock_user(user_id: int):
    """
    can unblock: admin only
    :param user_id:
    :return: unblocked user
    """
    pass