]# Spring 핵심 개념

Spring의 핵심 개념에는 IoC, DI, AOP, PSA가 있다.

Spring은 이러한 개념을 통해 객체의 생성과 관리를 편리하게 하고, 특정 기술에 대한 의존성을 줄여 POJO 기반의 개발을 할 수 있도록 도와준다.

## 1. IoC (Inversion of Control)

IoC는 Inversion of Control의 약자로, 제어의 역전이라는 의미이다.

일반적인 Java 프로그램에서는 개발자가 필요한 객체를 직접 생성하고 관리한다.

`public class A {
    private B b = new B();
}`

위 코드에서는 `A` 클래스가 `new B()`를 통해 필요한 `B` 객체를 직접 생성하고 있다.

Spring에서는 개발자가 객체를 직접 생성하고 관리하는 대신 Spring Container가 객체를 생성하고 관리할 수 있다.

Spring Container가 생성하고 관리하는 객체를 Bean(빈)이라고 한다.

예를 들어 `@Component`, `@Service`, `@Repository` 등의 어노테이션을 사용하면 해당 클래스를 Spring이 Bean으로 등록하고 관리할 수 있다.

`@Service
public class UserService {
}`

즉, 객체를 생성하고 관리하는 제어권이 개발자의 코드에서 Spring Container로 넘어가는 것을 IoC(제어의 역전)라고 한다.

IoC = 객체의 생성과 관리에 대한 제어권을 개발자가 직접 가지는 것이 아니라 외부(Spring Container)에 맡기는 개념

---

## 2. DI (Dependency Injection)

DI는 Dependency Injection의 약자로, 의존성 주입이라는 의미이다.

한 객체가 다른 객체의 기능을 사용해야 하는 경우 두 객체 사이에 의존 관계가 있다고 한다.

예를 들어 `UserService`에서 `UserRepository`의 기능이 필요하다면 `UserService`는 `UserRepository`에 의존한다고 할 수 있다.

`@Service
public class UserService {

```
private final UserRepository userRepository;

public UserService(UserRepository userRepository) {
    this.userRepository = userRepository;
}
```

}`

위 코드에서는 `UserService`가 직접 `new UserRepository()`를 사용하여 객체를 생성하지 않는다.

대신 Spring Container가 관리하고 있는 `UserRepository` 객체를 `UserService`의 생성자를 통해 넣어준다.

이처럼 필요한 객체를 직접 생성하는 것이 아니라 외부에서 전달받는 것을 DI(의존성 주입)라고 한다.

Spring에서는 생성자 주입이나 `@Autowired` 등을 이용하여 의존성을 주입할 수 있다.

IoC와 DI는 서로 관련되어 있으며, IoC라는 개념을 구현하는 대표적인 방법 중 하나가 DI이다.

DI = 객체가 필요로 하는 다른 객체를 직접 생성하지 않고 외부에서 주입받는 것

---

## 3. AOP (Aspect Oriented Programming)

AOP는 Aspect Oriented Programming의 약자로, 관점 지향 프로그래밍이라는 의미이다.

프로그램을 개발하다 보면 여러 기능에서 공통적으로 사용되는 코드가 발생한다.

예를 들어 회원가입, 로그인, 게시글 작성 등의 기능마다 실행 기록을 남기는 로깅 코드가 필요할 수 있다.

`회원가입 → 로깅 + 회원가입 로직
로그인 → 로깅 + 로그인 로직
게시글 → 로깅 + 게시글 작성 로직`

이렇게 여러 기능에서 반복되는 로깅 등의 코드를 각각 작성하면 중복 코드가 많아진다.

AOP는 프로그램의 기능을 핵심 관점과 부가 관점으로 나누어 공통적으로 사용되는 기능을 분리한다.

* 핵심 관점: 회원가입, 로그인, 계좌 이체 등 프로그램의 핵심 기능
* 부가 관점: 로깅, 트랜잭션 처리 등 여러 기능에서 공통적으로 필요한 기능

AOP를 사용하면 공통 기능을 핵심 로직에서 분리할 수 있기 때문에 코드의 중복을 줄이고 유지보수를 쉽게 할 수 있다.

AOP = 여러 곳에서 반복되는 공통 기능을 핵심 로직과 분리하여 관리하는 개념

---

## 4. PSA (Portable Service Abstraction)

PSA는 Portable Service Abstraction의 약자로, 이식 가능한 서비스 추상화라는 의미이다.

Spring에서는 여러 기술의 복잡한 사용 방법을 추상화하여 개발자가 일관된 방식으로 사용할 수 있도록 한다.

예를 들어 데이터베이스에 접근할 때 JDBC, JPA, MyBatis 등 여러 기술을 사용할 수 있다.

각각 내부적으로 동작하는 방식에는 차이가 있지만 Spring은 이러한 기술들을 쉽게 사용할 수 있도록 추상화된 방식을 제공한다.

또한 사용하는 기술이나 실행 환경이 변경되더라도 애플리케이션의 핵심 코드를 최대한 적게 수정할 수 있도록 도와준다.

이렇게 특정 기술의 복잡한 부분을 감추고 일관된 방식으로 사용할 수 있도록 하는 것을 PSA라고 한다.

PSA = 서로 다른 기술을 추상화하여 개발자가 일관된 방식으로 사용할 수 있도록 하는 개념
