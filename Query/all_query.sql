CREATE TABLE Authors (
    author_id INT IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
GO

CREATE TABLE Books (
    book_id INT IDENTITY PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author_id INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    FOREIGN KEY(author_id) REFERENCES Authors(author_id)
);
GO

CREATE TABLE Customers (
    customer_id INT IDENTITY PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);
GO

CREATE TABLE Orders (
    order_id INT IDENTITY PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATETIME DEFAULT GETDATE(),
    FOREIGN KEY(customer_id) REFERENCES Customers(customer_id)
);
GO

CREATE TABLE OrderItems (
    order_id INT NOT NULL,
    book_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    PRIMARY KEY(order_id, book_id),
    FOREIGN KEY(order_id) REFERENCES Orders(order_id),
    FOREIGN KEY(book_id) REFERENCES Books(book_id)
);
GO

-- Індекси
CREATE NONCLUSTERED INDEX idx_books_title ON Books(title);
GO
CREATE NONCLUSTERED INDEX idx_authors_name ON Authors(name);
GO
CREATE NONCLUSTERED INDEX idx_customers_email ON Customers(email);
GO

-- Функція для обрахунку загальної суми замовлення
CREATE FUNCTION fn_OrderTotal(@order_id INT)
RETURNS DECIMAL(10,2)
AS
BEGIN
    DECLARE @total DECIMAL(10,2);
    SELECT @total = SUM(b.price * oi.quantity)
    FROM OrderItems oi
    JOIN Books b ON b.book_id = oi.book_id
    WHERE oi.order_id = @order_id;

    RETURN ISNULL(@total,0);
END;
GO

-- Тригер на вставку в OrderItems, що оновлює склад
CREATE TRIGGER trg_OrderItems_Insert
ON OrderItems
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (
        SELECT 1
        FROM inserted i
        JOIN Books b ON b.book_id = i.book_id
        WHERE b.stock < i.quantity
    )
    BEGIN
        RAISERROR ('Недостатньо книг на складі',16,1);
        ROLLBACK TRANSACTION;
        RETURN;
    END

    UPDATE Books
    SET stock = stock - i.quantity
    FROM inserted i
    WHERE Books.book_id = i.book_id;
END;
GO

