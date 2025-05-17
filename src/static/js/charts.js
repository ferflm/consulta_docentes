const colores = ['#001E5A', '#C5911E'];

// Gráfico 1: Profesores por categoría (horizontal)
const getOptionChart1 = () => {
    const categorias = categoriaData.map(item => item[0]);
    const valores = categoriaData.map(item => item[1]);

    return {
        title: {
            text: 'Profesores por Categoría',
            left: 'center',
            top: 10,
            textStyle: { fontSize: 16 }
        },
        color: ['#C5911E'],
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: { type: 'value' },
        yAxis: {
            type: 'category',
            data: categorias,
            axisLabel: { interval: 0, fontSize: 12 }
        },
        series: [{
            name: 'Profesores',
            type: 'bar',
            data: valores,
            barWidth: '60%'
        }]
    };
};

// Gráfico 2: Distribución por género (pastel)
const getOptionChart2 = () => {
    const datos = generoData.map(item => ({ value: item[1], name: item[0] }));

    return {
        title: {
            text: 'Distribución por Género',
            left: 'center',
            top: 10,
            textStyle: { fontSize: 16 }
        },
        color: colores,
        tooltip: { trigger: 'item' },
        legend: {
            orient: 'horizontal',
            top: 'bottom',  // Mueve la leyenda debajo del gráfico
            textStyle: { fontSize: 14 }
        },
        series: [{
            name: 'Género',
            type: 'pie',
            radius: ['40%', '60%'],  // Reduce un poco para que no se desborde
            center: ['50%', '45%'],  // Centrado arriba
            avoidLabelOverlap: false,
            itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
            },
            label: { show: false },
            emphasis: {
                label: {
                    show: true,
                    fontSize: 20,
                    fontWeight: 'bold'
                }
            },
            labelLine: { show: false },
            data: datos
        }]
    };
};


// Gráfico 3: Profesores por grado académico (horizontal)
const getOptionChart3 = () => {
    const grados = gradoData.map(item => item[0]);
    const valores = gradoData.map(item => item[1]);

    return {
        title: {
            text: 'Profesores por Grado Académico',
            left: 'center',
            top: 10,
            textStyle: { fontSize: 16 }
        },
        color: colores,
        tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'shadow' }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: { type: 'value' },
        yAxis: {
            type: 'category',
            data: grados,
            axisLabel: { fontSize: 12 }
        },
        series: [{
            name: 'Profesores',
            type: 'bar',
            data: valores,
            barWidth: '50%'
        }]
    };
};

// Inicializa todos los gráficos
const initCharts = () => {
    const chart1 = echarts.init(document.getElementById('chart1'));
    const chart2 = echarts.init(document.getElementById('chart2'));
    const chart3 = echarts.init(document.getElementById('chart3'));

    chart1.setOption(getOptionChart1());
    chart2.setOption(getOptionChart2());
    chart3.setOption(getOptionChart3());

    // Responsivo
    window.addEventListener('resize', () => {
        chart1.resize();
        chart2.resize();
        chart3.resize();
    });
};

window.addEventListener('load', initCharts);
