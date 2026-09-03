# JPA란?

### JPA는 Java Persistence API의 약자로, Java에서 객체와 데이터베이스를 연결하기 위한 ORM 표준 기술이다.

### JPA 자체는 하나의 표준(규칙)이며, 이를 실제로 구현한 대표적인 구현체로 Hibernate(하이버네이트)​가 있다.

## ORM이란?

### ORM은 Object Relational Mapping의 약자로, Java의 객체와 관계형 데이터베이스의 테이블을 연결하는 기술이다.

## JPA를 사용하는 이유

직접 SQL을 작성하는 방식은 객체가 변경될 때 SQL도 수정해야 하는 **SQL 의존성 문제**와 객체와 DB의 구조가 다른 **패러다임 불일치** 문제가 있다.

JPA는 객체와 DB를 매핑하여 이러한 문제를 줄여준다.

## Entity

Entity는 **JPA가 DB와 연결하여 관리하는 객체**이다.

* `@Entity`: Entity 지정
* `@Id`: PK 지정
* `@GeneratedValue`: PK 자동 생성
* `@Column`: 컬럼 설정

## Spring Data JPA

Spring Data JPA는 **Spring에서 JPA를 편리하게 사용할 수 있도록 도와주는 기술**이다.

`JpaRepository`를 상속하면 SQL을 직접 작성하지 않아도 기본적인 CRUD 기능을 사용할 수 있다.

