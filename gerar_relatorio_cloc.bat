@echo off
setlocal EnableDelayedExpansion

:: Define codificação UTF-8
chcp 65001 > nul

echo === CONTADOR DE LINHAS DE CÓDIGO - SCRIPT SIMPLIFICADO ===
echo.

:: Verificar se cloc está instalado
where cloc >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERRO: A ferramenta 'cloc' não foi encontrada no sistema.
    echo Por favor, instale o cloc usando um dos métodos abaixo:
    echo.
    echo 1. Via npm: npm install -g cloc
    echo 2. Via chocolatey: choco install cloc
    echo 3. Baixe o executável em: https://github.com/AlDanial/cloc/releases/
    echo.
    pause
    exit /b 1
)

:: Preparar pasta para o relatório (no local atual)
set "PASTA_RELATORIO=cloc_resultado"

if not exist "%PASTA_RELATORIO%" (
    mkdir "%PASTA_RELATORIO%"
    echo ✅ Pasta "%PASTA_RELATORIO%" criada com sucesso.
) else (
    echo ✅ Pasta "%PASTA_RELATORIO%" já existe.
)

:: Definir nome do arquivo de relatório
set "DATA_ATUAL=%date:~6,4%-%date:~3,2%-%date:~0,2%"
set "ARQUIVO_RELATORIO=%PASTA_RELATORIO%\relatorio_%DATA_ATUAL%.txt"

echo.
echo === Executando contagem de linhas de código ===
echo O relatório será salvo em: "%ARQUIVO_RELATORIO%"
echo.

:: Mudar para o diretório do script e executar cloc a partir dali
pushd "%~dp0"

:: Executar cloc no diretório atual (.)
echo Executando: cloc . --exclude-dir=venv,dist,build,__pycache__ --out="%ARQUIVO_RELATORIO%"
cloc . --exclude-dir=venv,dist,build,__pycache__ --out="%ARQUIVO_RELATORIO%" 2>&1
set CLOC_STATUS=%errorlevel%

:: Voltar ao diretório original
popd

:: Verificar o resultado
echo.
if %CLOC_STATUS% neq 0 (
    echo ❌ Ocorreu um erro ao executar o cloc (código: %CLOC_STATUS%)
) else (
    if exist "%ARQUIVO_RELATORIO%" (
        :: Adicionar informações extras ao relatório
        echo ✅ Relatório gerado com sucesso.
        echo.
        echo === Adicionando informações adicionais ao relatório ===
        (
            echo.
            echo ==========================================
            echo Observações adicionais:
            echo - Relatório gerado em: %DATE% %TIME%
            echo - Projeto: Rabisco - Editor de Texto
            echo - Pastas ignoradas: venv, dist, build, __pycache__
            echo ==========================================
        ) >> "%ARQUIVO_RELATORIO%"
        
        :: Mostrar conteúdo do relatório
        echo.
        echo === CONTEÚDO DO RELATÓRIO ===
        type "%ARQUIVO_RELATORIO%"
        echo.
        
        :: Perguntar se quer abrir o relatório
        set /p ABRIR_RELATORIO="Deseja abrir o relatório no bloco de notas? (S/N): "
        if /i "!ABRIR_RELATORIO!"=="S" start notepad "%ARQUIVO_RELATORIO%"
    ) else (
        echo ❌ Não foi possível encontrar o arquivo de relatório.
    )
)

echo.
echo Pressione qualquer tecla para sair...
pause > nul
exit /b