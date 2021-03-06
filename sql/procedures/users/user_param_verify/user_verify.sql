USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS USER_VERIFY;
CREATE PROCEDURE USER_VERIFY(
    IN vUSER_ID INT,
    IN vLOGIN VARCHAR(255),
    IN vEMAIL VARCHAR(255),
    IN vROLE VARCHAR(255),
    OUT vRESCODE INT,
    OUT vMSG VARCHAR(255)
)
COMMENT 'Проверяет уникальность переданных vLOGIN, vEMAIL,
        существование роли vROLE
        (т.е. возможность добавить или изменить пользователя).
        В качестве vUSER_ID передавать:
            - 0: при проверки возможности добавить пользователя;
            - USER_ID: при проверки возможности изменить пользователя.
            
        Возвращает:
            - vRESCODE:
                0 - в случае ошибки,
                1 - в случае успешной верификации;
            - vMSG:
                сообщение об ошибке.'
PROC : BEGIN
    -- Проверка существования роли
    SET @roleid = NULL;
    SELECT
            R.role_id
        INTO
            @roleid
        FROM
            role as R
        WHERE
            R.NAME = vROLE;
    
    IF @roleid IS NULL THEN
        SET vRESCODE = 0;
        SET vMSG = CONCAT('Роль не существует: ', vROLE);
        LEAVE PROC;
    END IF;
    
    -- Проверка на уникальность нового логина
    SET @existing_login = NULL;
    SELECT
            U.LOGIN
        INTO
            @existing_login
        FROM
            user as U
        WHERE
            U.LOGIN = vLOGIN AND
            U.USER_ID != vUSER_ID;
            
    IF @existing_login IS NOT NULL THEN
        SET vRESCODE = 0;
        SET vMSG = CONCAT('Логин уже занят: ', @existing_login);
    LEAVE PROC;
    END IF;
    
    -- Проверка на уникальность нового адрес эл.почты
    SET @existing_email = NULL;
    SELECT
            U.EMAIL
        INTO
            @existing_email
        FROM
            user as U
        WHERE
            U.EMAIL = vEMAIL AND
            U.USER_ID != vUSER_ID;
            
    IF @existing_email IS NOT NULL THEN
        SET vRESCODE = 0;
        SET vMSG = CONCAT('email уже занят: ', @existing_email);
        LEAVE PROC;
    END IF;
    
    -- Данные корректны:
    SELECT 1, '' INTO vRESCODE, vMSG;
END
$$

DELIMITER ;
