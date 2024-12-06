import React, { useState, useEffect } from 'react';
import * as XLSX from 'xlsx';
import { Pie, Bar } from 'react-chartjs-2';
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale, BarElement } from 'chart.js';

// Registrar los componentes necesarios de Chart.js
ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale, BarElement);

const Statistics = () => {
    const [productsData, setProductsData] = useState([]);
    const [selectedYear, setSelectedYear] = useState("");
    const [selectedInvestigator, setSelectedInvestigator] = useState("");
    const [selectedType, setSelectedType] = useState("");

    useEffect(() => {
        // Función para leer el archivo Excel
        const readExcel = async () => {
            try {
                const response = await fetch('/resultados_investigadoresAUltimate.xlsx');
                const arrayBuffer = await response.arrayBuffer();
                const wb = XLSX.read(arrayBuffer, { type: 'array' });
                const wsname = wb.SheetNames[0];
                const ws = wb.Sheets[wsname];
                const data = XLSX.utils.sheet_to_json(ws);

                const formattedData = data.map((item, index) => ({
                    id: index.toString(),
                    investigador: item['INVESTIGADOR'],
                    titulo: item['TÍTULO DEL PRODUCTO'],
                    tipo: item['TIPO DEL PRODUCTO'],
                    ano: item['AÑO'],
                    archivo: item['NOMBRE DEL ARCHIVO'],
                    link: item['link archivo']
                }));

                setProductsData(formattedData);
            } catch (error) {
                console.error('Error loading Excel file:', error);
            }
        };

        readExcel();
    }, []);

    // Filtrar productos según los filtros seleccionados
    const filteredProducts = productsData.filter(product => {
        const matchesYear = selectedYear === "" || product.ano === selectedYear;
        const matchesInvestigator = selectedInvestigator === "" || product.investigador.toLowerCase().includes(selectedInvestigator.toLowerCase());
        const matchesType = selectedType === "" || product.tipo === selectedType;
        return matchesYear && matchesInvestigator && matchesType;
    });

    const years = [...new Set(productsData.map(product => product.ano))];
    const investigators = [...new Set(productsData.map(product => product.investigador))];
    const types = [...new Set(productsData.map(product => product.tipo))];

    // Preparar los datos para los gráficos
    const yearCounts = years.map(year => {
        return filteredProducts.filter(product => product.ano === year).length;
    });

    const investigatorCounts = investigators.map(investigator => {
        return filteredProducts.filter(product => product.investigador === investigator).length;
    });

    const typeCounts = types.map(type => {
        return filteredProducts.filter(product => product.tipo === type).length;
    });

    const pieData = {
        labels: types,
        datasets: [
            {
                data: typeCounts,
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#FF9F40'],
            },
        ],
    };

    const barData = {
        labels: years,
        datasets: [
            {
                label: 'Productos por Año',
                data: yearCounts,
                backgroundColor: '#36A2EB',
            },
        ],
    };

    return (
        <div className="bg-slate-950 p-4 text-white">
            <h2>Estadísticas de Productos</h2>

            {/* Filtros */}
            <div className="mb-4">
                <label>Año:</label>
                <select onChange={(e) => setSelectedYear(e.target.value)} value={selectedYear}>
                    <option value="">Todos los años</option>
                    {years.map(year => (
                        <option key={year} value={year}>{year}</option>
                    ))}
                </select>

                <label className="ml-4">Investigador:</label>
                <input
                    type="text"
                    placeholder="Buscar investigador"
                    value={selectedInvestigator}
                    onChange={(e) => setSelectedInvestigator(e.target.value)}
                    className="ml-2 p-2"
                />

                <label className="ml-4">Tipo de Producto:</label>
                <select onChange={(e) => setSelectedType(e.target.value)} value={selectedType}>
                    <option value="">Todos los tipos</option>
                    {types.map(type => (
                        <option key={type} value={type}>{type}</option>
                    ))}
                </select>
            </div>

            {/* Estadísticas */}
            <div>
                <p><strong>Total de Productos:</strong> {filteredProducts.length}</p>
                <p><strong>Total de Tipos de Producto Únicos:</strong> {types.length}</p>
                <p><strong>Total de Investigadores Únicos:</strong> {investigators.length}</p>
                <p><strong>Total de Años Únicos:</strong> {years.length}</p>
            </div>

            {/* Gráficos */}
            <div className="mt-4">
                <h3>Distribución de Tipos de Productos</h3>
                <Pie data={pieData} />

                <h3 className="mt-8">Productos por Año</h3>
                <Bar data={barData} />
            </div>
        </div>
    );
};

export default Statistics;
