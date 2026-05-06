# 게시판 api 명세서


• **POST** `/api/auth/signup` : 회원가입 (아이디, 비밀번호, 닉네임 입력)

• **POST** `/api/auth/login` : 로그인 (성공 시 토큰이나 세션 반환)

• **POST** `/api/auth/logout` : 로그아웃

• **GET** `/api/users/me` : 내 정보 조회 (마이페이지용)

• **PATCH** `/api/users/me` : 회원 정보 수정 (비밀번호나 닉네임 변경)

• **DELETE** `/api/users/me` : 회원 탈퇴

• **GET** `/api/posts` : 전체 게시글 목록 조회


• **GET** `/api/posts/search` : 게시글 검색


• **POST** `/api/posts` : 게시글 작성 (제목, 내용, 카테고리, 이미지 등)

• **GET** `/api/posts/{postId}` : 게시글 상세 내용 조회 (조회수 1 증가 포함)

• **PUT** `/api/posts/{postId}` : 게시글 수정 (작성자 본인만 가능)

• **DELETE** `/api/posts/{postId}` : 게시글 삭제 

• **GET** `/api/posts/{postId}/comments` : 특정 게시글의 댓글 목록 조회

• **POST** `/api/posts/{postId}/comments` : 댓글 작성

• **DELETE** `/api/comments/{commentId}` : 댓글 삭제

• **POST** `/api/posts/{postId}/like` : 게시글 좋아요/취소 

• **GET** `/api/admin/users` : 전체 회원 목록 관리
