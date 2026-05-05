import uuid
from datetime import datetime, timezone

from .database import SessionLocal
from .models import Post, Comment, Room, User
from .auth import hash_password

# 고정 UUID (서버 재시작마다 동일한 데이터가 들어가도록)
POST_IDS = [
    "a1b2c3d4-0001-0001-0001-000000000001",
    "a1b2c3d4-0002-0002-0002-000000000002",
    "a1b2c3d4-0003-0003-0003-000000000003",
    "a1b2c3d4-0004-0004-0004-000000000004",
    "a1b2c3d4-0005-0005-0005-000000000005",
]
COMMENT_IDS = [
    "b2c3d4e5-00c1-00c1-00c1-0000000000c1",
    "b2c3d4e5-00c2-00c2-00c2-0000000000c2",
    "b2c3d4e5-00c3-00c3-00c3-0000000000c3",
    "b2c3d4e5-00c4-00c4-00c4-0000000000c4",
    "b2c3d4e5-00c5-00c5-00c5-0000000000c5",
    "b2c3d4e5-00c6-00c6-00c6-0000000000c6",
    "b2c3d4e5-00c7-00c7-00c7-0000000000c7",
    "b2c3d4e5-00c8-00c8-00c8-0000000000c8",
]
ROOM_IDS = [
    "c3d4e5f6-0001-0001-0001-000000000001",
    "c3d4e5f6-0002-0002-0002-000000000002",
    "c3d4e5f6-0003-0003-0003-000000000003",
    "c3d4e5f6-0004-0004-0004-000000000004",
    "c3d4e5f6-0005-0005-0005-000000000005",
    "c3d4e5f6-0006-0006-0006-000000000006",
    "c3d4e5f6-0007-0007-0007-000000000007",
    "c3d4e5f6-0008-0008-0008-000000000008",
    "c3d4e5f6-0009-0009-0009-000000000009",
    "c3d4e5f6-0010-0010-0010-000000000010",
]
ADMIN_ID = "d4e5f6a7-ad00-ad00-ad00-000000000ad0"


def seed_initial_data():
    db = SessionLocal()
    try:
        if db.query(Post).count() > 0:
            return

        posts_data = [
            {
                "id": POST_IDS[0],
                "title": "커뮤니티에 오신 것을 환영합니다!",
                "content": "안녕하세요! 이곳은 자유롭게 소통하는 커뮤니티입니다. 궁금한 점이나 나누고 싶은 이야기를 자유롭게 작성해주세요.",
                "author": "관리자",
                "created_at": datetime(2026, 3, 20, 9, 0, tzinfo=timezone.utc),
                "likes": 5,
                "comments": [
                    {"id": COMMENT_IDS[0], "content": "반갑습니다! 잘 부탁드려요 😊", "author": "수빈", "created_at": datetime(2026, 3, 20, 10, 30, tzinfo=timezone.utc)},
                    {"id": COMMENT_IDS[1], "content": "커뮤니티 오픈 축하해요!", "author": "민준", "created_at": datetime(2026, 3, 20, 11, 15, tzinfo=timezone.utc)},
                ],
            },
            {
                "id": POST_IDS[1],
                "title": "Next.js 공부하는 분 계신가요?",
                "content": "요즘 Next.js App Router를 공부하고 있는데, 같이 스터디하실 분 있으면 댓글 남겨주세요! 매주 토요일 오후에 온라인으로 진행하려고 합니다.",
                "author": "지원",
                "created_at": datetime(2026, 3, 21, 14, 20, tzinfo=timezone.utc),
                "likes": 12,
                "comments": [
                    {"id": COMMENT_IDS[2], "content": "저도 관심 있어요! 참여하고 싶습니다.", "author": "하은", "created_at": datetime(2026, 3, 21, 15, 0, tzinfo=timezone.utc)},
                    {"id": COMMENT_IDS[3], "content": "토요일 오후 몇 시에 하나요?", "author": "서준", "created_at": datetime(2026, 3, 21, 16, 45, tzinfo=timezone.utc)},
                    {"id": COMMENT_IDS[4], "content": "저도 끼워주세요~", "author": "수빈", "created_at": datetime(2026, 3, 22, 9, 10, tzinfo=timezone.utc)},
                ],
            },
            {
                "id": POST_IDS[2],
                "title": "오늘 점심 뭐 먹을까요",
                "content": "학교 앞에 새로 생긴 돈까스 집 가본 사람 있나요? 맛있다고 해서 가보려는데 후기 궁금합니다!",
                "author": "민준",
                "created_at": datetime(2026, 3, 22, 11, 30, tzinfo=timezone.utc),
                "likes": 3,
                "comments": [
                    {"id": COMMENT_IDS[5], "content": "거기 치즈돈까스 진짜 맛있어요 강추!", "author": "지원", "created_at": datetime(2026, 3, 22, 11, 50, tzinfo=timezone.utc)},
                ],
            },
            {
                "id": POST_IDS[3],
                "title": "React useState 질문이요",
                "content": "useState로 상태를 변경했는데 바로 console.log를 찍으면 이전 값이 나와요. 왜 그런 건가요? 비동기인가요?",
                "author": "하은",
                "created_at": datetime(2026, 3, 23, 16, 0, tzinfo=timezone.utc),
                "likes": 8,
                "comments": [
                    {"id": COMMENT_IDS[6], "content": "맞아요! setState는 비동기로 동작해서, 다음 렌더링에서 반영돼요. useEffect로 변경된 값을 확인할 수 있어요.", "author": "서준", "created_at": datetime(2026, 3, 23, 16, 30, tzinfo=timezone.utc)},
                    {"id": COMMENT_IDS[7], "content": "저도 처음에 이거 때문에 엄청 헤맸어요 ㅋㅋ", "author": "민준", "created_at": datetime(2026, 3, 23, 17, 0, tzinfo=timezone.utc)},
                ],
            },
            {
                "id": POST_IDS[4],
                "title": "TypeScript 처음 쓰는데 어렵네요",
                "content": "JavaScript만 쓰다가 TypeScript 처음 써보는데 타입 에러가 너무 많이 뜹니다... 익숙해지면 편해지나요?",
                "author": "서준",
                "created_at": datetime(2026, 3, 24, 10, 0, tzinfo=timezone.utc),
                "likes": 15,
                "comments": [],
            },
        ]

        for post_data in posts_data:
            comments_data = post_data.pop("comments")
            post = Post(**post_data)
            db.add(post)
            db.flush()

            for comment_data in comments_data:
                comment = Comment(**comment_data, post_id=post.id)
                db.add(comment)

        db.commit()

        seed_rooms(db)
        seed_admin_user(db)
    finally:
        db.close()


def seed_rooms(db):
    if db.query(Room).count() > 0:
        return

    rooms = [
        Room(
            id=ROOM_IDS[0], name="스터디룸 A", location="3층 301호", capacity=4,
            description="4인용 소규모 스터디룸",
            amenities=["화이트보드", "모니터", "Wi-Fi"],
        ),
        Room(
            id=ROOM_IDS[1], name="스터디룸 B", location="3층 302호", capacity=8,
            description="8인용 중규모 스터디룸",
            amenities=["화이트보드", "프로젝터", "Wi-Fi"],
        ),
        Room(
            id=ROOM_IDS[2], name="스터디룸 C", location="4층 401호", capacity=6,
            description="6인용 스터디룸 (조용한 구역)",
            amenities=["화이트보드", "Wi-Fi"],
        ),
        Room(
            id=ROOM_IDS[3], name="대회의실", location="5층 501호", capacity=20,
            description="20인용 대회의실",
            amenities=["프로젝터", "마이크", "스피커", "Wi-Fi"],
        ),
        Room(
            id=ROOM_IDS[4], name="스터디룸 D", location="3층 303호", capacity=2,
            description="2인용 미니 스터디룸",
            amenities=["모니터", "Wi-Fi"],
        ),
        Room(
            id=ROOM_IDS[5], name="스터디룸 E", location="4층 402호", capacity=10,
            description="10인용 세미나룸",
            amenities=["화이트보드", "프로젝터", "모니터", "Wi-Fi"],
        ),
        Room(
            id=ROOM_IDS[6], name="미디어룸", location="4층 403호", capacity=6,
            description="영상 시청 및 발표 연습용",
            amenities=["프로젝터", "스피커", "마이크", "Wi-Fi"],
        ),
        Room(
            id=ROOM_IDS[7], name="스터디룸 F", location="5층 502호", capacity=4,
            description="4인용 스터디룸 (창가석)",
            amenities=["화이트보드", "Wi-Fi"],
        ),
        Room(
            id=ROOM_IDS[8], name="그룹 토론실", location="5층 503호", capacity=12,
            description="12인용 원형 토론실",
            amenities=["화이트보드", "모니터", "마이크", "Wi-Fi"],
        ),
        Room(
            id=ROOM_IDS[9], name="오픈 스페이스", location="6층 601호", capacity=30,
            description="30인용 오픈형 공유 공간",
            amenities=["프로젝터", "마이크", "스피커", "화이트보드", "Wi-Fi"],
        ),
    ]
    db.add_all(rooms)
    db.commit()


def seed_admin_user(db):
    admin = db.query(User).filter(User.role == "admin").first()
    if admin:
        return

    admin_user = User(
        id=ADMIN_ID,
        username="admin",
        email="admin@study.com",
        hashed_password=hash_password("admin123"),
        role="admin",
    )
    db.add(admin_user)
    db.commit()
