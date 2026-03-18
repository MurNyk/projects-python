// Constants for material coefficients
const MATERIAL_COEFFICIENTS = {
    "Медь": 0.85,
    "Алюминий": 0.75,
    "Прутья": 0.90,
    "Листы металла": 0.80,
    "Трубы": 0.78,
    "Проволока": 0.92,
    "Блоки": 0.70,
    "Детали": 0.88,
    "Пластины": 0.81,
    "Профили": 0.76,
    "Катанка": 0.84,
    "Рельсы": 0.82,
    "Ленты": 0.77,
    "Балка": 0.74,
    "Арматура": 0.79,
    "Корпусные изделия": 0.87,
    "Металлические профили": 0.83,
    "Металлические сетки": 0.86,
    "Фольга": 0.72
};

// Функция для получения коэффициента переработки на основе выбранного материала
function getMaterialCoefficient(material) {
    return MATERIAL_COEFFICIENTS[material] || 1; // По умолчанию 1, если материал неизвестен
}

// Функция для расчета коэффициента переработки
function calculateProcessingCoefficient() {
    const inputQuantity = parseFloat(document.getElementById('quantity').value);
    const outputQuantity = parseFloat(document.getElementById('output_quantity').value);
    const selectedMaterial = document.getElementById('final_product').value;
    
    console.log("Входное количество:", inputQuantity);
    console.log("Выходное количество:", outputQuantity);
    console.log("Выбранный материал:", selectedMaterial);

    const materialCoefficient = getMaterialCoefficient(selectedMaterial);

    // Проверяем корректность введенных данных
    if (!isNaN(inputQuantity) && !isNaN(outputQuantity) && inputQuantity > 0 && outputQuantity >= 0) {
        // Рассчитываем коэффициент с учетом материала
        const coefficient = (outputQuantity / inputQuantity) * materialCoefficient;
        document.getElementById('processing_coefficient').value = coefficient.toFixed(2); // Округляем до двух знаков
    } else {
        document.getElementById('processing_coefficient').value = '0.00'; // Устанавливаем значение по умолчанию
    }
}

// Привязываем функцию расчета к полям ввода
document.getElementById('final_product').addEventListener('change', calculateProcessingCoefficient);
document.getElementById('quantity').addEventListener('input', calculateProcessingCoefficient);
document.getElementById('output_quantity').addEventListener('input', calculateProcessingCoefficient);