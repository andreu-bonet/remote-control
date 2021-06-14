
export interface ConfigService {
	set(key: string, value: any): void
	get(key: string, defaultValue?: any): any
	exists(key: string): boolean
}
