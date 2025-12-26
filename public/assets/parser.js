// parser.js
import { v4 as uuidv4 } from 'uuid';
import { createLogger } from '../utils/logger';

const logger = createLogger('Parser');

class Parser {
  constructor() {
    this.parsers = {
      json: JSON.parse,
      xml: (data) => new DOMParser().parseFromString(data, 'text/xml'),
      csv: (data) => {
        const lines = data.split('\n');
        const csvData = [];
        const headers = lines.shift().split(',');
        for (const line of lines) {
          const row = {};
          const values = line.split(',');
          for (let i = 0; i < headers.length; i++) {
            row[headers[i]] = values[i];
          }
          csvData.push(row);
        }
        return csvData;
      },
      binary: () => {
        throw new Error('Binary parsing is not supported');
      },
    };
  }

  async parse(data, type) {
    if (!this.parsers[type]) {
      throw new Error(`Unsupported format: ${type}`);
    }
    try {
      return this.parsers[type](data);
    } catch (error) {
      logger.error('Error parsing data:', error);
      throw error;
    }
  }

  async uploadFile(file) {
    const id = uuidv4();
    const fileBuffer = await file.arrayBuffer();
    const fileType = file.type;
    const fileSize = file.size;
    const parser = new Parser();
    const data = await parser.parse(fileBuffer, fileType.split('/')[1]);
    return { id, data, fileType, fileSize };
  }
}

export default Parser;