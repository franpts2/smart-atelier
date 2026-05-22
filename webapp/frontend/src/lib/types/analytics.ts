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

export interface DualRulesetDistribution {
    standard: DistributionItem[];
    advanced: DistributionItem[];
}

export interface DualRulesetComparison {
    standard: ModelMetric[];
    advanced: ModelMetric[];
}
