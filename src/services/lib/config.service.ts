import { ConfigService } from '../../types/config.service'


export class LocalConfigService implements ConfigService {
	private config: { [key: string]: any }

	constructor(private dotenv: any) {
		this.dotenv.config()
		this.config = Object.assign({}, process.env)
	}

	public set(key: string, value: any): void {
		this.config[key] = value
	}

	public get(key: string, defaultValue?: any): any {
		return this.exists(key) ? this.config[key] : defaultValue
	}

	public exists(key: string): boolean {
		return this.config[key] !== undefined
	}
}
