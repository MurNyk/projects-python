// Функция для переключения полей формы в зависимости от выбранного типа ремонта
function toggleFormFields() {
    const repairType = document.getElementById('repair_type').value;

    // Скрываем все секции сначала
    document.getElementById('vehicle_fields').style.display = 'none';
    document.getElementById('tools_fields').style.display = 'none';
    document.getElementById('machines_fields').style.display = 'none';
    
    // Показываем соответствующую секцию
    if (repairType === 'vehicle') {
      document.getElementById('vehicle_fields').style.display = 'block';
    } else if (repairType === 'tools') {
      document.getElementById('tools_fields').style.display = 'block';
    } else if (repairType === 'machines') {
      document.getElementById('machines_fields').style.display = 'block';
    }
}