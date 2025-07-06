document.addEventListener('DOMContentLoaded', () => {
    const chartContainer = document.getElementById('chart');
    const chart = LightweightCharts.createChart(chartContainer, {
        width: chartContainer.clientWidth,
        height: chartContainer.clientHeight,
        layout: {
            background: { type: 'solid', color: 'black' },
            textColor: '#d1d5db',
        },
        grid: {
            vertLines: { visible: false },         
            horzLines: { visible: false },          // No grid lines
        },
        priceScale: {
            borderColor: '#555',
        },
        timeScale: {
            visible: true,
            borderColor: '#555',
            timeVisible: true,
            secondsVisible: true,
        },
        crosshair: {
            mode: LightweightCharts.CrosshairMode.Normal,
        },
    });

    // Candlestick series (Bid OHLC)
    const candleSeries = chart.addCandlestickSeries({
        upColor: '#10b981',
        downColor: '#ef4444',
        borderUpColor: '#10b981',
        borderDownColor: '#ef4444',
        wickUpColor: '#10b981',
        wickDownColor: '#ef4444',
    });

    // Bid price line (Blue)
    const bidPriceLine = candleSeries.createPriceLine({
        price: 0,
        color: '#3b82f6',          // Blue for Bid
        lineWidth: 1,
        lineStyle: LightweightCharts.LineStyle.Solid,
        axisLabelVisible: true,
        title: 'Bid',
    });

    // Ask price line (Red)
    const askPriceLine = candleSeries.createPriceLine({
        price: 0,
        color: '#ef4444',          // Red for Ask
        lineWidth: 1,
        lineStyle: LightweightCharts.LineStyle.Solid,
        axisLabelVisible: true,
        title: 'Ask',
    });

    window.addEventListener('resize', () => {
        chart.resize(chartContainer.clientWidth, chartContainer.clientHeight);
    });

    const candles = {};
    const timeframeSeconds = timeframe;

    // Aggregate ticks into OHLC candles
    function aggregateTick(tick) {
        const tickTime = Number(tick.time); // Use API time, ensure number
        const bucketTime = Math.floor(tickTime / timeframeSeconds) * timeframeSeconds;

        if (!candles[bucketTime]) {
            // New candle
            candles[bucketTime] = {
                time: bucketTime,
                open: tick.bid,
                high: tick.bid,
                low: tick.bid,
                close: tick.bid,
            };
            console.log('🕯️ New candle created at', new Date(bucketTime * 1000).toISOString());
        } else {
            // Update existing candle
            let candle = candles[bucketTime];
            candle.high = Math.max(candle.high, tick.bid);
            candle.low = Math.min(candle.low, tick.bid);
            candle.close = tick.bid;
            console.log('🔄 Updated candle:', candle);
        }

        const lastCandle = candles[bucketTime];
        candleSeries.update({
            time: Number(lastCandle.time),
            open: lastCandle.open,
            high: lastCandle.high,
            low: lastCandle.low,
            close: lastCandle.close,
        });
    }

    // Load historical candles and then start live updates
    function loadHistoryAndStart() {
        console.log('📦 Loading historical candles from:', historyUrl);

        fetch(historyUrl)
            .then(res => {
                console.log('📥 Raw response:', res);
                return res.json();
            })
            .then(data => {
                console.log("✅ History data received:", data);
                data.forEach(c => {
                    candles[Number(c.time)] = {
                        time: Number(c.time),
                        open: c.open,
                        high: c.high,
                        low: c.low,
                        close: c.close,
                    };
                });

                candleSeries.setData(
                    data.map(c => ({
                        time: Number(c.time),
                        open: c.open,
                        high: c.high,
                        low: c.low,
                        close: c.close,
                    }))
                );

                startWebSocket();
            })
            .catch(err => {
                console.error('⚠️ Failed to load history:', err);
                startWebSocket();
            });
    }

    // Start WebSocket for live ticks
    function startWebSocket() {
        console.log('🔌 Connecting to WebSocket:', priceApiUrl);
        const socket = new WebSocket(priceApiUrl);

        socket.addEventListener('open', () => {
            console.log('✅ Connected to WebSocket:', priceApiUrl);
        });

        socket.addEventListener('message', (event) => {
            console.log('📡 WebSocket raw tick:', event.data);

            let tick;
            try {
                tick = JSON.parse(event.data);
                console.log('✅ Parsed tick:', tick);
            } catch (e) {
                console.error('❌ Failed to parse tick:', e);
                return;
            }

            if (!tick.bid || !tick.ask || !tick.time) {
                console.warn('⚠️ Tick missing bid/ask/time:', tick);
                return;
            }

            // Update candle with Bid price
            aggregateTick(tick);

            // Update Bid and Ask price lines
            bidPriceLine.applyOptions({
                price: tick.bid,
            });
            askPriceLine.applyOptions({
                price: tick.ask,
            });
        });

        socket.addEventListener('close', () => {
            console.log('❌ WebSocket closed');
        });

        socket.addEventListener('error', (error) => {
            console.error('⚠️ WebSocket error:', error);
        });
    }

    // 🚀 Start
    loadHistoryAndStart();
});
