import dotenv from 'dotenv'
import { LocalConfigService } from './lib/config.service'
import { ConfigService } from '../types/config.service'

const configService: ConfigService = new LocalConfigService(dotenv)

export default configService
