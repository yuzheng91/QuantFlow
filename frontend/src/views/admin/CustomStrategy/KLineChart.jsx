// KLineChart.jsx
import React, { useEffect, useRef, useState } from 'react';
import { createChart } from 'lightweight-charts';
import Papa from 'papaparse';

const KLineChart = ({ signals = [] }) => {
  const chartRef = useRef();
  const [data, setData] = useState([]);

  // 讀取 CSV
  useEffect(() => {
    fetch('/data/MSFT.csv')
      .then((response) => response.text())
      .then((csvText) => {
        const parsed = Papa.parse(csvText, { header: true });
        const formatted = parsed.data
          .filter(
            (row) => row.Date && row.Open && row.High && row.Low && row.Close,
          )
          .map((row) => ({
            time: row.Date.trim(), // 格式如 "2022-01-01"
            open: parseFloat(row.Open),
            high: parseFloat(row.High),
            low: parseFloat(row.Low),
            close: parseFloat(row.Close),
          }));
        setData(formatted);
      });
  }, []);

  // 建立圖表與加上 signals
  useEffect(() => {
    if (!chartRef.current || data.length === 0) return;

    const chart = createChart(chartRef.current, {
      width: chartRef.current.clientWidth,
      height: chartRef.current.clientHeight,
    });

    const series = chart.addCandlestickSeries();
    series.setData(data);

    // 加上進出場標記
    const markers = signals.map((sig) => ({
      time: sig.time, // 必須跟 data 中的 time 一致
      position: sig.signal === 'buy' ? 'belowBar' : 'aboveBar',
      color: sig.signal === 'buy' ? 'green' : 'red',
      shape: sig.signal === 'buy' ? 'arrowUp' : 'arrowDown',
      text: sig.signal,
    }));
    series.setMarkers(markers);

    // 自動 resize
    const handleResize = () => {
      chart.resize(chartRef.current.clientWidth, chartRef.current.clientHeight);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      chart.remove();
      window.removeEventListener('resize', handleResize);
    };
  }, [data, signals]);

  return <div ref={chartRef} style={{ width: '100%', height: '100%' }} />;
};

export default KLineChart;
