from datetime import datetime, timezone

from .database import SessionLocal
from .models import Post, Comment, Room, User
from .auth import hash_password


def seed_initial_data():
    db = SessionLocal()
    try:
        if db.query(Post).count() > 0:
            return

        posts_data = [
            {
                "id": "1",
                "title": "커뮤니티에 오신 것을 환영합니다!",
                "content": "안녕하세요! 이곳은 자유롭게 소통하는 커뮤니티입니다. 궁금한 점이나 나누고 싶은 이야기를 자유롭게 작성해주세요.",
                "author": "관리자",
                "created_at": datetime(2026, 3, 20, 9, 0, tzinfo=timezone.utc),
                "likes": 5,
                "comments": [
                    {"id": "c1", "content": "반갑습니다! 잘 부탁드려요 😊", "author": "수빈", "created_at": datetime(2026, 3, 20, 10, 30, tzinfo=timezone.utc)},
                    {"id": "c2", "content": "커뮤니티 오픈 축하해요!", "author": "민준", "created_at": datetime(2026, 3, 20, 11, 15, tzinfo=timezone.utc)},
                ],
            },
            {
                "id": "2",
                "title": "Next.js 공부하는 분 계신가요?",
                "content": "요즘 Next.js App Router를 공부하고 있는데, 같이 스터디하실 분 있으면 댓글 남겨주세요! 매주 토요일 오후에 온라인으로 진행하려고 합니다.",
                "author": "지원",
                "created_at": datetime(2026, 3, 21, 14, 20, tzinfo=timezone.utc),
                "likes": 12,
                "comments": [
                    {"id": "c3", "content": "저도 관심 있어요! 참여하고 싶습니다.", "author": "하은", "created_at": datetime(2026, 3, 21, 15, 0, tzinfo=timezone.utc)},
                    {"id": "c4", "content": "토요일 오후 몇 시에 하나요?", "author": "서준", "created_at": datetime(2026, 3, 21, 16, 45, tzinfo=timezone.utc)},
                    {"id": "c5", "content": "저도 끼워주세요~", "author": "수빈", "created_at": datetime(2026, 3, 22, 9, 10, tzinfo=timezone.utc)},
                ],
            },
            {
                "id": "3",
                "title": "오늘 점심 뭐 먹을까요",
                "content": "학교 앞에 새로 생긴 돈까스 집 가본 사람 있나요? 맛있다고 해서 가보려는데 후기 궁금합니다!",
                "author": "민준",
                "created_at": datetime(2026, 3, 22, 11, 30, tzinfo=timezone.utc),
                "likes": 3,
                "comments": [
                    {"id": "c6", "content": "거기 치즈돈까스 진짜 맛있어요 강추!", "author": "지원", "created_at": datetime(2026, 3, 22, 11, 50, tzinfo=timezone.utc)},
                ],
            },
            {
                "id": "4",
                "title": "React useState 질문이요",
                "content": "useState로 상태를 변경했는데 바로 console.log를 찍으면 이전 값이 나와요. 왜 그런 건가요? 비동기인가요?",
                "author": "하은",
                "created_at": datetime(2026, 3, 23, 16, 0, tzinfo=timezone.utc),
                "likes": 8,
                "comments": [
                    {"id": "c7", "content": "맞아요! setState는 비동기로 동작해서, 다음 렌더링에서 반영돼요. useEffect로 변경된 값을 확인할 수 있어요.", "author": "서준", "created_at": datetime(2026, 3, 23, 16, 30, tzinfo=timezone.utc)},
                    {"id": "c8", "content": "저도 처음에 이거 때문에 엄청 헤맸어요 ㅋㅋ", "author": "민준", "created_at": datetime(2026, 3, 23, 17, 0, tzinfo=timezone.utc)},
                ],
            },
            {
                "id": "5",
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
            id="room_1", name="스터디룸 A", location="3층 301호", capacity=4,
            description="4인용 소규모 스터디룸",
            amenities=["화이트보드", "모니터", "Wi-Fi"],
        ),
        Room(
            id="room_2", name="스터디룸 B", location="3층 302호", capacity=8,
            description="8인용 중규모 스터디룸",
            amenities=["화이트보드", "프로젝터", "Wi-Fi"],
        ),
        Room(
            id="room_3", name="스터디룸 C", location="4층 401호", capacity=6,
            description="6인용 스터디룸 (조용한 구역)",
            amenities=["화이트보드", "Wi-Fi"],
        ),
        Room(
            id="room_4", name="대회의실", location="5층 501호", capacity=20,
            description="20인용 대회의실",
            amenities=["프로젝터", "마이크", "스피커", "Wi-Fi"],
        ),
        Room(
            id="room_5", name="스터디룸 D", location="3층 303호", capacity=2,
            description="2인용 미니 스터디룸",
            amenities=["모니터", "Wi-Fi"],
        ),
        Room(
            id="room_6", name="스터디룸 E", location="4층 402호", capacity=10,
            description="10인용 세미나룸",
            amenities=["화이트보드", "프로젝터", "모니터", "Wi-Fi"],
        ),
        Room(
            id="room_7", name="미디어룸", location="4층 403호", capacity=6,
            description="영상 시청 및 발표 연습용",
            amenities=["프로젝터", "스피커", "마이크", "Wi-Fi"],
        ),
        Room(
            id="room_8", name="스터디룸 F", location="5층 502호", capacity=4,
            description="4인용 스터디룸 (창가석)",
            amenities=["화이트보드", "Wi-Fi"],
        ),
        Room(
            id="room_9", name="그룹 토론실", location="5층 503호", capacity=12,
            description="12인용 원형 토론실",
            amenities=["화이트보드", "모니터", "마이크", "Wi-Fi"],
        ),
        Room(
            id="room_10", name="오픈 스페이스", location="6층 601호", capacity=30,
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
        id=f"user_{int(datetime.now(timezone.utc).timestamp() * 1000)}",
        username="admin",
        email="admin@study.com",
        hashed_password=hash_password("admin123"),
        role="admin",
    )
    db.add(admin_user)
    db.commit()
