<?php
// pdf_viewer.php
$file = htmlspecialchars($_GET['file'] ?? '');

if (empty($file) || !file_exists($file) || strtolower(pathinfo($file, PATHINFO_EXTENSION)) !== 'pdf') {
    // Se o arquivo não existir ou não for um PDF, exibe uma mensagem
    die("Arquivo PDF não encontrado ou inválido.");
}

// Redireciona para o viewer.html, usando a sintaxe de path relativo ao viewer.html
// O `urlencode` é crucial para lidar com nomes de arquivos com espaços.
// O `../` é necessário porque o viewer.html está DENTRO da pasta 'web'.
header("Location: web/viewer.html?file=" . urlencode("../" . $file));
exit;
?>