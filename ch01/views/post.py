from fastapi import APIRouter
from uuid import UUID, uuid1

from models.post import Post, PostType
from models.forum import ForumPost, ForumDiscussion
from views.user import valid_users, discussion_posts, valid_profiles
from views.account import user_does_not_exist


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}}
)


@router.post("/add/{username}")
async def post_discussion(username: str, post: Post, post_type: PostType):
    if valid_users.get(username) is None:
        return user_does_not_exist()

    if discussion_posts.get(id) is not None:
        return {"message": "post already exists"}

    forum_post = ForumPost(id=uuid1(), 
                           topic=post.topic, 
                           message=post.message, 
                           post_type=post_type,
                           date_posted=post.date_posted,
                           username=username)
    user = valid_profiles[username]
    forum = ForumDiscussion(id=uuid1(), main_post=forum_post, author=user, replies=list())
    discussion_posts[forum.id] = forum
    return forum


@router.post("/reply/{username}")
async def post_reply(username: str, id: UUID, post_type: PostType, post_reply: Post):
    if valid_users.get(username) is None:
        return user_does_not_exist()

    if discussion_posts.get(id) is None:
        return post_does_not_exist()

    reply = ForumPost(id=uuid1(),
                      topic=post_reply.topic,
                      message=post_reply.message,
                      post_type=post_type,
                      date_posted=post_reply.date_posted,
                      username=username)
    main_post = discussion_posts[id]
    main_post.replies.append(reply)
    return reply


@router.get("/view/{username}")
async def view_discussion(username: str, id: UUID):
    if valid_users.get(username) is None:
        return user_does_not_exist()

    if discussion_posts.get(id) is None:
        return post_does_not_exist()

    forum = discussion_posts[id]
    return forum


@router.put("/update/{username}")
async def update_discussion(username: str, id: UUID, post_type: PostType, post: Post):
    if valid_users.get(username) is None:
        return user_does_not_exist()

    if discussion_posts.get(id) is None:
        return post_does_not_exist()

    forum_post = ForumPost(id=uuid1(), 
                           topic=post.topic, 
                           message=post.message, 
                           post_type=post_type, 
                           date_posted=post.date_posted, 
                           username=username)
    forum = discussion_posts[id]
    forum.main_post = forum_post
    return {"message": "main post updated"}


@router.delete("/remove/{username}")
async def delete_discussion(username: str, id: UUID):
    if valid_users.get(username) is None:
        return user_does_not_exist()

    if discussion_posts.get(id) is None:
        return post_does_not_exist()

    del discussion_posts[id]
    return {"message": "main post deleted"}


# helper methods   
def post_does_not_exist():
    return {"message": "post does not exist"}