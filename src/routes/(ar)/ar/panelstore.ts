import { writable } from 'svelte/store';
import type { Asset } from '../../../types';

export const currentAsset = writable<Asset | null>(null);
