Write-Host "Iniciando Backend..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'c:\Users\Miguel\Desktop\Miguelon\Work\CompanypcaMacroProcesos\PCA_Facturacion_BackEnd'; npm run server"
Write-Host "Iniciando Frontend..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'c:\Users\Miguel\Desktop\Miguelon\Work\CompanypcaMacroProcesos\PCA_Facturacion_Frontend'; npm run start"
