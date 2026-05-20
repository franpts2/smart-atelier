export interface DistributionItem {
    label: string;
    count: number;
}

export interface ModelMetric {
    id: string;
    name: string;
    accuracy: number;
    precision: number;
    recall: number;
    f1_score: number;
}
