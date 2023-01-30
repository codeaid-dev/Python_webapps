<?php
$isbn = "";
$name = "";
$price = "";
$page = "";
$date = "";
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
  list($errors, $input) = validate_form();
  if ($errors) {
    print 'これらのエラーを修正してください。<ul><li>';
    print implode('</li><li>', $errors);
    print '</li></ul>';
    //exit();
  } else {
    //$dsn = 'mysql:host=localhost;dbname=bookstore;charset=utf8'; // XAMPP/MAMP/VMの場合
    $dsn = 'mysql:host=mysql;dbname=bookstrage;charset=utf8'; // Dockerの場合
    //$dsn = 'sqlite:./bookstrage.db'; // SQLiteの場合
    $user = 'root';
    $password = 'password';

    try {
      $db = new PDO($dsn, $user, $password);
      //$db = new PDO($dsn); //SQLiteの場合
      $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false); // prepareを使用する際のSQLインジェクション対策(必須)
      $db->query("CREATE TABLE IF NOT EXISTS books (
        isbn VARCHAR(17) NOT NULL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        price INT NOT NULL,
        page INT NOT NULL,
        date VARCHAR(255) NOT NULL
      ) DEFAULT CHARACTER SET=utf8;");

      $res = $db->query("SELECT * FROM books WHERE isbn='$isbn'");
      if (count($res->fetchAll()) != 0) {
        print '<p>入力したISBNはすでに保存されています。</p>';
      } else {
        $stmt = $db->prepare("INSERT INTO books (isbn, name, price, page, date) VALUES (:isbn, :name, :price, :page, :date)");
        $stmt->bindParam(':isbn', $isbn, PDO::PARAM_STR);
        $stmt->bindParam(':name', $name, PDO::PARAM_STR);
        $stmt->bindParam(':price', $price, PDO::PARAM_INT);
        $stmt->bindParam(':page', $page, PDO::PARAM_INT);
        $stmt->bindParam(':date', $date, PDO::PARAM_STR);
        $stmt->execute();
        print '<p>保存できました。</p>';
      }
    } catch (PDOException $e) {
      die ('エラー：'.$e->getMessage());
    }
  }
}

function validate_form() {
  $input['isbn'] = filter_input(INPUT_POST, 'isbn', FILTER_VALIDATE_INT);
  $input['price'] = filter_input(INPUT_POST, 'price', FILTER_VALIDATE_INT);
  $input['page'] = filter_input(INPUT_POST, 'page', FILTER_VALIDATE_INT);
  $errors = array();
  if (empty($input['isbn'])) {
    $errors[] = 'ISBNは数字で入力してください。';
  } else {
    $GLOBALS['isbn'] = htmlspecialchars($_POST['isbn']);
  }
  if (empty($_POST['name'])) {
    $errors[] = '書籍名を入力してください。';
  } else {
    $GLOBALS['name'] = htmlspecialchars($_POST['name']);
  }
  if (empty($input['price'])) {
    $errors[] = '価格は数字を入力してください。';
  } else {
    $GLOBALS['price'] = htmlspecialchars($_POST['price']);
  }
  if (empty($input['page'])) {
    $errors[] = 'ページ数は数字を入力してください。';
  } else {
    $GLOBALS['page'] = htmlspecialchars($_POST['page']);
  }
  if (empty($_POST['date'])) {
    $errors[] = '発売日を入力してください。';
  } else {
    $GLOBALS['date'] = htmlspecialchars($_POST['date']);
  }

  return array($errors, $input);
}
?>
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>書籍データ庫</title>
</head>
<body>
  <h1>書籍データ庫</h1>
  <form action="<?= htmlspecialchars($_SERVER['PHP_SELF']) ?>" method="POST">
    <p><label>ISBN：<input type="text" name="isbn" value=<?= htmlspecialchars($isbn) ?>></label></p>
    <p><label>書籍名：<input type="text" name="name" value=<?= htmlspecialchars($name) ?>></label></p>
    <p><lave>価格：<input type="text" name="price" value=<?= htmlspecialchars($price) ?>></lave></p>
    <p><lave>ページ数：<input type="text" name="page" value=<?= htmlspecialchars($page) ?>></lave></p>
    <p><lave>発売日：<input type="date" name="date" value=<?= htmlspecialchars($date) ?>></lave></p>
    <button type="submit">保存</button>
  </form>
  <p><span style="margin-right: 30px"><a href="index.html">トップ</a></span><a href="read.php">閲覧ページ</a></p>
</body>
</html>