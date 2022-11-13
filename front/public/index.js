import { LocationProvider, Router, Route, lazy, ErrorBoundary, hydrate, prerender as ssr } from 'preact-iso';
import Session from './pages/session/index.js';
import NotFound from './pages/_404.js';
import Header from './header.js';
import {AuthProvider} from './context/auth';
import { ToastProvider } from './context/toast.js';
import Toast from './components/toast/index.js';

const Home = lazy(() => import('./pages/home/index.js'));
const Sessions = lazy(() => import('./pages/sessions/index.js'));
const Remote = lazy(() => import('./pages/remote/index.js'));

export function App() {
	return (
		<AuthProvider>
			<ToastProvider>
				<LocationProvider>
					<div class="app">
						<Header />
						<ErrorBoundary>
							<Router>
								<Route path="/" component={Home} />
								<Route path="/sessions" component={Sessions} />
								<Route path="/session/:id" component={Session} />
								<Route path="/remote" component={Remote} />
								<Route default component={NotFound} />
							</Router>
						</ErrorBoundary>
						<Toast 
							position="top-right"
						/>
					</div>
				</LocationProvider>
			</ToastProvider>
		</AuthProvider>
	);
}

hydrate(<App />);

export async function prerender(data) {
	return await ssr(<App {...data} />);
}
