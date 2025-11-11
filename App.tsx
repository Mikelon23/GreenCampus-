
import React, { useState, useEffect, useRef } from 'react';
import Header from './components/Header';
import MetricCard from './components/MetricCard';
import HistoryChart from './components/HistoryChart';
import SummaryCard from './components/SummaryCard';
import { useSimulatedApi } from './hooks/useSimulatedApi';
import { CO2Icon, EnergyIcon, HumidityIcon, TemperatureIcon, LeafIcon, ClockIcon } from './components/Icons';
import { useAuth } from './AuthContext';
import { getMessaging, getToken, onMessage } from 'firebase/messaging';
import { app, VAPID_KEY, isFirebaseConfigured } from './firebaseConfig';


// A simple toast notification component for in-app alerts
const NotificationToast: React.FC<{ message: string; onDismiss: () => void; type?: 'danger' | 'success' }> = ({ message, onDismiss, type = 'danger' }) => {
    useEffect(() => {
        const timer = setTimeout(onDismiss, 6000);
        return () => clearTimeout(timer);
    }, [onDismiss]);

    const bgColor = type === 'danger' ? 'bg-danger' : 'bg-primary';

    return (
        <div className={`w-80 p-4 rounded-lg shadow-lg text-white ${bgColor} animate-fade-in-down`}>
            <div className="flex items-start justify-between">
                <p className="font-semibold">{message}</p>
                <button onClick={onDismiss} className="text-xl font-bold leading-none">&times;</button>
            </div>
        </div>
    );
};


const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const { latestData, historicalData, isLoading: dataIsLoading } = useSimulatedApi(!!user);
  const [notifications, setNotifications] = useState<{id: number, message: string, type: 'danger' | 'success'}[]>([]);
  const alertState = useRef({ co2: false, temperature: false, energy: false });

  const addNotification = (message: string, type: 'danger' | 'success' = 'danger') => {
    const newId = Date.now();
    setNotifications(prev => [...prev, { id: newId, message, type }]);
  };

  const dismissNotification = (id: number) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  };
  
  // Effect for Firebase Cloud Messaging setup
  useEffect(() => {
    const setupNotifications = async () => {
        // IMPORTANT: Push notifications require a `firebase-messaging-sw.js` file.
        // This setup will likely fail without it, but the code demonstrates the process.
        if (!isFirebaseConfigured || !('Notification' in window) || !('serviceWorker' in navigator)) {
            console.warn("Push notifications not supported or Firebase not configured.");
            return;
        }

        try {
            const messaging = getMessaging(app);
            const permission = await Notification.requestPermission();
            
            if (permission === 'granted') {
                console.log('Notification permission granted.');
                const currentToken = await getToken(messaging, { vapidKey: VAPID_KEY });
                if (currentToken) {
                    console.log('FCM Token:', currentToken);
                    addNotification("Registered for push notifications!", 'success');
                } else {
                    console.log('No registration token available.');
                }
            } else {
                console.log('Unable to get permission to notify.');
            }

            onMessage(messaging, (payload) => {
                console.log('Message received in foreground: ', payload);
                if (payload.notification?.title && payload.notification?.body) {
                   addNotification(`${payload.notification.title}: ${payload.notification.body}`);
                }
            });

        } catch (err) {
            console.error('An error occurred while setting up notifications: ', err);
            addNotification("Could not register for push notifications.");
        }
    };

    setupNotifications();
  }, []);

  // Effect for monitoring thresholds and creating in-app alerts
  useEffect(() => {
    if (!latestData) return;
    const { co2, temperature, energy } = latestData;

    // CO2 Alert
    if (co2 > 1000 && !alertState.current.co2) {
        addNotification(`High CO₂ Alert: ${co2.toFixed(0)} ppm`);
        alertState.current.co2 = true;
    } else if (co2 <= 800 && alertState.current.co2) {
        alertState.current.co2 = false; // Reset when back to normal
    }

    // Temperature Alert
    if (temperature > 30 && !alertState.current.temperature) {
        addNotification(`High Temperature Alert: ${temperature.toFixed(1)}°C`);
        alertState.current.temperature = true;
    } else if (temperature <= 25 && alertState.current.temperature) {
        alertState.current.temperature = false;
    }

    // Energy Alert
    if (energy > 200 && !alertState.current.energy) {
        addNotification(`High Energy Usage: ${energy.toFixed(1)} kWh`);
        alertState.current.energy = true;
    } else if (energy <= 150 && alertState.current.energy) {
        alertState.current.energy = false;
    }
  }, [latestData]);


  const averageCO2 = historicalData.length > 0
    ? (historicalData.reduce((sum, data) => sum + data.co2, 0) / historicalData.length).toFixed(0)
    : '...';

  const sustainabilityScore = () => {
    if (!latestData) return '0.0';
    let score = 100;
    if (latestData.co2 > 800) score -= (latestData.co2 - 800) / 20;
    if (latestData.temperature > 25) score -= (latestData.temperature - 25) * 2;
    if (latestData.energy > 150) score -= (latestData.energy - 150) / 5;
    
    return Math.max(0, Math.min(100, score)).toFixed(1);
  };
  
  if (dataIsLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-base-300 text-white">
        <div className="text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary mx-auto mb-4"></div>
            <h1 className="text-2xl font-bold">Initializing GreenCampus+ Dashboard...</h1>
            <p>Connecting to environmental sensors.</p>
        </div>
      </div>
    );
  }

  return (
     <div className="min-h-screen bg-base-300 font-sans">
      <div className="fixed top-5 right-5 z-50 space-y-3">
        {notifications.map((n) => (
            <NotificationToast key={n.id} message={n.message} type={n.type} onDismiss={() => dismissNotification(n.id)} />
        ))}
      </div>
      <Header />
      <main className="p-4 sm:p-6 lg:p-8">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
          <MetricCard
            label="Temperature"
            value={latestData?.temperature.toFixed(1) ?? '...'}
            unit="°C"
            icon={<TemperatureIcon />}
            thresholds={{ warn: 25, danger: 30 }}
            currentValue={latestData?.temperature}
          />
          <MetricCard
            label="Humidity"
            value={latestData?.humidity.toFixed(1) ?? '...'}
            unit="%"
            icon={<HumidityIcon />}
            thresholds={{ warn: 60, danger: 70 }}
            currentValue={latestData?.humidity}
          />
          <MetricCard
            label="CO₂ Levels"
            value={latestData?.co2.toFixed(0) ?? '...'}
            unit="ppm"
            icon={<CO2Icon />}
            thresholds={{ warn: 800, danger: 1000 }}
            currentValue={latestData?.co2}
          />
          <MetricCard
            label="Energy Usage"
            value={latestData?.energy.toFixed(1) ?? '...'}
            unit="kWh"
            icon={<EnergyIcon />}
            thresholds={{ warn: 150, danger: 200 }}
            currentValue={latestData?.energy}
          />
        </div>

        <div className="mt-6 grid grid-cols-1 xl:grid-cols-3 gap-6">
          <div className="xl:col-span-1 space-y-6">
            <SummaryCard 
                icon={<LeafIcon />}
                title="Sustainability Score"
                value={sustainabilityScore()}
                description="Overall campus eco-rating. Higher is better."
            />
            <SummaryCard
                icon={<CO2Icon />}
                title="Avg. CO₂ (24h)"
                value={`${averageCO2} ppm`}
                description="Average CO₂ concentration over the last 24 hours."
            />
             <SummaryCard
                icon={<ClockIcon />}
                title="Last Updated"
                value={latestData ? new Date(latestData.timestamp).toLocaleTimeString() : '...'}
                description="Data is refreshed automatically every 5 seconds."
            />
          </div>
          <div className="xl:col-span-2 bg-base-200 p-4 rounded-xl shadow-lg">
             <HistoryChart 
                data={historicalData}
              />
          </div>
        </div>
      </main>
    </div>
  )
}

const App: React.FC = () => {
  return <Dashboard />;
};

export default App;