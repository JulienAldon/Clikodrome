import { LocationProvider, Router, Route, lazy, ErrorBoundary, hydrate, prerender as ssr } from 'preact-iso';
import Session from './pages/session/index.js';
import NotFound from './pages/_404.js';
import Header from './header.js';
import {AuthProvider} from './context/auth';
import { ToastProvider } from './context/toast.js';
import Toast from './components/toast/index.js';
import './i18n';
import Footer from './pages/footer/index.js';

const Home = lazy(() => import('./pages/home/index.js'));
const Sessions = lazy(() => import('./pages/sessions/index.js'));
const Remote = lazy(() => import('./pages/remote/index.js'));
const Manager = lazy(() => import('./pages/manager/index.js'));
const Promotion = lazy(() => import('./pages/promotion/index.js'));

export function App() {
	return (
		<AuthProvider>
			<ToastProvider>
				<LocationProvider>
					<div className="app wrapper">
						<Header />
						<ErrorBoundary>
							<Router>
								<Route path="/" component={Home} />
								<Route path="/sessions/:city?" component={Sessions} />
								<Route path="/session/:id" component={Session} />
								<Route path="/promotion/:id" component={Promotion} />
								<Route path="/remote/:city?" component={Remote} />
								<Route path="/manager/:city?" component={Manager} />
								<Route default component={NotFound} />
							</Router>
						</ErrorBoundary>
						<Toast />
						<Footer></Footer>
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