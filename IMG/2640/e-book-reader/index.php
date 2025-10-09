<?php
error_reporting(E_ERROR | E_PARSE);

// Configurações e Funções PHP
// Versão mínima recomendada para este script: PHP 7.4 ou superior

// 1. Definições
$allowed_extensions = ['pdf', 'png', 'jpg', 'jpeg'];
$current_dir = __DIR__; 
$file_list = [];
$cover_file = null; 
$default_file = null; 

// --- LÓGICA DE COOKIE CORRIGIDA PARA JSON ÚNICO (ESTADO COMPLETO) ---
// Substitui 'last_ebook_file' e 'last_ebook_page' por um único cookie JSON
$cookie_state_name = 'ebook_state'; 
$cookie_expire = time() + (86400 * 30); // 30 dias

// Títulos (Mantendo as variáveis do arquivo que você enviou)
$main_title = "Leitor de E-book";
$subtitle = "Livro: O Dia Mais Frio";

// 2. Função para formatar o nome do arquivo
function format_filename($filename) {
    $name_without_ext = pathinfo($filename, PATHINFO_FILENAME);
    $readable_name = str_replace(['-', '_'], ' ', $name_without_ext);
    $formatted_name = ucwords(strtolower($readable_name));
    return $formatted_name;
}

// 3. Listar e filtrar arquivos
try {
    $files = scandir($current_dir);
    foreach ($files as $file) {
        if ($file === '.' || $file === '..') {
            continue;
        }

        $extension = strtolower(pathinfo($file, PATHINFO_EXTENSION));

        if (in_array($extension, $allowed_extensions)) {
            if (in_array($file, ['capa.jpg', 'capa.png', 'cover.jpg', 'cover.png'])) {
                $cover_file = $file;
                continue; 
            }
            
            $file_list[] = [
                'full_name' => $file,
                'display_name' => format_filename($file),
                'extension' => $extension
            ];
            if ($default_file === null) {
                $default_file = $file;
            }
        }
    }
} catch (Exception $e) {
    die("Erro ao ler o diretório: " . $e->getMessage());
}

// 4. Lógica de Carregamento: APENAS 2 PASSOS DE PRIORIDADE (Cookie -> Capa)

$last_state = [];
$initial_load_file = null;

// Tenta ler o cookie JSON único
if (isset($_COOKIE[$cookie_state_name])) {
    $decoded_state = json_decode($_COOKIE[$cookie_state_name], true);
    if (json_last_error() === JSON_ERROR_NONE && is_array($decoded_state)) {
        $last_state = $decoded_state;
    }
}

$last_file_opened_from_cookie = $last_state['file'] ?? null;

// --- VALIDAÇÃO: Garante que o arquivo do cookie exista.
$validated_file = null;
if (isset($last_file_opened_from_cookie) && $last_file_opened_from_cookie !== "") {
    $file_to_check = urldecode($last_file_opened_from_cookie); 
    if (file_exists($file_to_check)) {
        $validated_file = $file_to_check;
    }
}

// =========================================================
// LÓGICA DE 2 PASSOS DE PRIORIDADE (COOKIE -> CAPA)
// =========================================================

// Prioridade 1: Cookie
if ($validated_file) {
    $initial_load_file = $validated_file;

// Prioridade 2: Capa
} elseif ($cover_file) {
    $initial_load_file = $cover_file;
}

// FALLBACK DE SEGURANÇA (Último Recurso)
if ($initial_load_file === null && $default_file !== null) {
    $initial_load_file = $default_file;
}

// Define o tipo inicial
$initial_type = 'pdf';
if ($initial_load_file) {
    $ext = pathinfo($initial_load_file, PATHINFO_EXTENSION);
    $initial_type = in_array(strtolower($ext), ['png', 'jpg', 'jpeg']) ? 'image' : 'pdf';
}

// Prepara o estado inicial completo para injeção no JS.
$initial_app_state_json = json_encode([
    'file' => $initial_load_file,
    'page' => ($last_state['file'] === $initial_load_file) ? ($last_state['page'] ?? 1) : 1,
    'zoom' => ($last_state['file'] === $initial_load_file) ? ($last_state['zoom'] ?? 'auto') : 'auto',
]);

?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= htmlspecialchars($main_title) ?></title>
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
    
    <style>
    /* Estilos customizados (Copiados EXATAMENTE do seu arquivo) */
    html, body {
        height: 100%;
        margin: 0;
        overflow: hidden; /* Garante que o body não role */
        background-color: #f2f2f2; 
    }
    .app-header {
        padding: 15px 20px 0;
        height: auto; 
        text-align: center; /* Centraliza o conteúdo (o wrapper) */
    }
    
    /* NOVO: Estilos Padrão (Mobile First - Títulos um embaixo do outro) */
    .header-titles-wrapper {
        /* Por padrão, os elementos H2 e H5 são blocos e ficam empilhados */
        display: block; 
        padding-bottom: 10px; /* Espaço para o main-container */
    }
    /* Centraliza o H2/H5 quando estão empilhados */
    .header-titles-wrapper h2, 
    .header-titles-wrapper h5 {
        margin-bottom: 0.5rem !important; /* Adiciona margem entre H2 e H5 quando empilhados */
    }

    
    /* REQUISITO ATENDIDO: Usa Flexbox APENAS quando houver espaço suficiente (telas > 768px) */
    @media (min-width: 769px) {
        .header-titles-wrapper {
            display: flex !important; /* Habilita o layout flexível */
            justify-content: center !important; /* Centraliza horizontalmente o grupo de títulos */
            align-items: baseline !important; /* Alinha os textos pela linha de base */
            gap: 15px !important; /* Espaço entre o H2 e o H5 */
        }
        /* Remove a margem extra entre eles quando estão lado a lado */
        .header-titles-wrapper h2, 
        .header-titles-wrapper h5 {
            margin-bottom: 0 !important; 
        }
    }
    
    .main-container {
        display: flex;
        height: calc(100vh - 80px); /* Altura padrão para telas grandes */
    }
    .content-area {
        flex-grow: 1; 
        padding: 0;
        overflow: hidden; 
        background-color: white; 
        box-shadow: 0 0 10px rgba(0,0,0,0.1); 
    }
    .sidebar {
        width: 250px; 
        height: 100%;
        overflow-y: auto; 
        background-color: #f8f9fa;
        border-right: 1px solid #dee2e6;
        padding: 15px;
    }
    iframe {
        width: 100%;
        height: 100%;
        border: none;
        background-color: white; 
    }
    
    /* Estilos de links permanecem os mesmos */
    .file-link {
        display: block;
        padding: 8px;
        margin-bottom: 5px;
        border-radius: 4px;
        text-decoration: none;
        color: #333;
        transition: background-color 0.2s;
    }
    .file-link:hover {
        background-color: #e9ecef;
        cursor: pointer;
    }
    .file-link.active {
        background-color: #0d6efd;
        color: white;
    }
    .file-icon {
        margin-right: 8px;
    }
    
    /* Media Query para Rodapé Móvel (Ajuste para telas menor que 769px) */
    @media (max-width: 768px) {
        .app-header {
            padding: 10px 10px 0;
        }

        /* Mantendo o cálculo da altura da sidebar/container que estava no seu arquivo */
        .main-container {
             height: calc(100vh - 120px); 
             flex-direction: column;
        }
        
        .sidebar {
            width: 100%;
            height: 80px; 
            overflow-x: auto;
            overflow-y: hidden;
            border-right: none;
            border-top: 1px solid #dee2e6;
            padding: 10px;
            white-space: nowrap; 
        }
        .file-link {
            display: inline-block; 
            width: auto;
        }
        .content-area {
            order: -1; 
            height: 100%;
        }
    }
</style>
</head>
<body>

<div class="app-header">
    <div class="header-titles-wrapper">
        <h2 class="text-primary mb-0"><?= htmlspecialchars($main_title) ?></h2>
        <h5 class="text-secondary mb-0"><?= htmlspecialchars($subtitle) ?></h5>
    </div>
</div>

<div class="main-container">
    
    <div class="sidebar d-flex flex-md-column align-items-md-start">
        <h6 class="text-secondary mb-3 d-none d-md-block">Capítulos e Arquivos</h6>
        
        <?php if (!empty($file_list) || $cover_file): ?>
            <?php
            // Capa
            if ($cover_file):
                $is_active = $initial_load_file === $cover_file ? 'active' : '';
            ?>
                <a href="#" class="file-link <?= $is_active ?>" 
                   data-file="<?= htmlspecialchars($cover_file) ?>"
                   data-type="image"
                   title="Capa do Livro">
                    <i class="fa-solid fa-book-open-reader text-warning file-icon"></i>
                    Capa do Livro
                </a>
            <?php endif; ?>

            <?php 
            // Capítulos
            foreach ($file_list as $file): 
                $ext = $file['extension'];
                $type = in_array($ext, ['png', 'jpg', 'jpeg']) ? 'image' : 'pdf';
                $icon_class = ($ext === 'pdf') ? 'fa-solid fa-file-pdf text-danger' : 'fa-solid fa-file-image text-success';
                $is_active = $file['full_name'] === $initial_load_file ? 'active' : '';
            ?>
                <a href="#" class="file-link <?= $is_active ?>" 
                   data-file="<?= htmlspecialchars($file['full_name']) ?>"
                   data-type="<?= $type ?>"
                   title="<?= htmlspecialchars($file['full_name']) ?>">
                    <i class="<?= $icon_class ?> file-icon"></i>
                    <?= htmlspecialchars($file['display_name']) ?>
                </a>
            <?php endforeach; ?>
        <?php else: ?>
            <p class="text-muted small">Nenhum conteúdo encontrado.</p>
        <?php endif; ?>
    </div>

    <div class="content-area">
        <?php if ($initial_load_file): ?>
            <iframe id="ebook-iframe" 
                    src="" 
                    title="Leitor de E-book">
            </iframe>
        <?php else: ?>
            <div class="alert alert-warning m-5" role="alert">
                <i class="fa-solid fa-triangle-exclamation"></i> Nenhum conteúdo para carregar.
            </div>
        <?php endif; ?>
    </div>
</div>

<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script>
$(document).ready(function() {
    const $iframe = $('#ebook-iframe');
    // --- Variáveis de Cookie DO NOVO SISTEMA ---
    const cookieStateName = 'ebook_state'; 
    const cookieExpireDays = 30;
    
    // Estado inicial injetado pelo PHP
    const initialAppState = <?= $initial_app_state_json ?>; 
    
    let currentAppState = initialAppState;
    let currentFileType = initialAppState.file ? (initialAppState.file.endsWith('.pdf') ? 'pdf' : 'image') : null;

    // ----------------------------------------------------
    // FUNÇÕES DE COOKIE (Sistema JSON Único)
    // ----------------------------------------------------
    function setCookie(name, value, days) {
        let expires = "";
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        // Usando o path=/ e SameSite=Lax para garantir a persistência
        document.cookie = name + "=" + encodeURIComponent(value) + expires + "; path=/; SameSite=Lax";
    }

    function getCookie(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for(let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) {
                return decodeURIComponent(c.substring(nameEQ.length, c.length));
            }
        }
        return null;
    }

    function setAppStateCookie(state) {
        setCookie(cookieStateName, JSON.stringify(state), cookieExpireDays);
    }

    // ----------------------------------------------------
    // FUNÇÃO DE CARREGAMENTO (Adaptação para Imagens e PDF)
    // ----------------------------------------------------
    function loadFileInIframe(fullPath, fileType, state) {
        currentFileType = fileType;
        currentAppState.file = fullPath;

        if (fileType === 'pdf') {
            // Salva o estado (page/zoom) na sessionStorage para que o pdf_viewer.php possa usá-lo
            sessionStorage.setItem('pdfjs_initial_state', JSON.stringify({
                page: state.page,
                zoom: state.zoom
            }));

            // Carrega o visualizador PDF
            $iframe.attr('src', 'pdf_viewer.php?file=' + encodeURIComponent(fullPath));

        } else if (fileType === 'image') {
            // Para imagens, usa o HTML simples para exibir a imagem
            const imageHtml = `
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body { margin: 0; background: #fff; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: auto;}
                        img { max-width: 100%; max-height: 100%; width: auto; height: auto; object-fit: contain; }
                    </style>
                </head>
                <body>
                    <img src="${fullPath}" alt="Documento de Imagem" />
                </body>
                </html>
            `;
            $iframe.attr('src', 'about:blank'); 
            $iframe.get(0).contentWindow.document.open();
            $iframe.get(0).contentWindow.document.write(imageHtml);
            $iframe.get(0).contentWindow.document.close();
            
            // Salva o estado para a imagem (page=1, zoom=auto)
            setAppStateCookie({ file: fullPath, page: 1, zoom: 'auto' });
        }
    }

    // ----------------------------------------------------
    // LISTENER DE MENSAGENS (COMUNICAÇÃO IFRAME -> PAI)
    // ----------------------------------------------------
    window.addEventListener('message', function(event) {
        if (event.data && event.data.type === 'PDF_STATE_UPDATE') {
            const newState = event.data.state;
            
            // Salva o estado completo (arquivo, página, zoom)
            const stateToSave = {
                file: currentAppState.file, 
                page: newState.page,
                zoom: newState.zoom
            };
            
            currentAppState = stateToSave;
            setAppStateCookie(currentAppState);
        }
    });

    // ----------------------------------------------------
    // LÓGICA DE INICIALIZAÇÃO
    // ----------------------------------------------------
    if (currentAppState.file) {
        // O estado inicial já foi injetado pelo PHP, basta carregar.
        loadFileInIframe(currentAppState.file, currentFileType, currentAppState);
    } 

    // ----------------------------------------------------
    // LÓGICA DE CLIQUE DE NAVEGAÇÃO
    // ----------------------------------------------------
    $('.file-link').on('click', function(e) {
        e.preventDefault();
        const $newLink = $(this);
        // Usa data-file e data-type (Conforme seu HTML)
        const fullPath = $newLink.data('file');
        const fileType = $newLink.data('type');

        // 1. Antes de carregar o novo arquivo, forçamos o iframe PDF a salvar seu estado.
        if (currentFileType === 'pdf' && $iframe.get(0) && $iframe.get(0).contentWindow) {
            try {
                // Pede o estado atual do PDF (e ele responde via postMessage, salvando o cookie)
                $iframe.get(0).contentWindow.postMessage({ type: 'GET_PDF_STATE' }, '*');
            } catch(error) {
                 console.error("Falha ao enviar mensagem GET_PDF_STATE:", error);
            }
        }
        
        // 2. CARREGAR O NOVO ARQUIVO
        
        // Busca o cookie *após* a potencial atualização acima (assíncrona, mas necessário para o estado de transição)
        const storedStateJson = getCookie(cookieStateName);
        const storedState = storedStateJson ? JSON.parse(storedStateJson) : {};
        
        const isSameFile = storedState.file === fullPath;

        const newState = {
            file: fullPath,
            // Se o arquivo for o mesmo que o salvo, usa o estado salvo; senão, reseta.
            page: isSameFile ? (storedState.page || 1) : 1,
            zoom: isSameFile ? (storedState.zoom || 'auto') : 'auto',
        };

        // Atualiza o link ativo
        $('.file-link').removeClass('active');
        $newLink.addClass('active');
        
        // Carrega o novo arquivo
        loadFileInIframe(fullPath, fileType, newState);
    });

    // --- Salvamento final ao fechar/recarregar a página principal ---
    $(window).on('beforeunload', function() {
        if (currentFileType === 'pdf' && $iframe.get(0) && $iframe.get(0).contentWindow) {
            try {
                // Mensagem final para garantir que o PDF salve o estado antes de fechar
                $iframe.get(0).contentWindow.postMessage({ type: 'GET_PDF_STATE_FINAL' }, '*');
            } catch(error) {
                 // Erro no beforeunload é comum e geralmente ignorável
            }
        }
    });

});
</script>
</body>
</html>