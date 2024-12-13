// Fungsi untuk menghitung evaluasi
function calculatePrecision(relevance) {
    const totalRelevance = relevance.reduce((sum, val) => sum + val, 0);
    return relevance.map((val, index) => {
        const relevantRetrieved = relevance.slice(0, index + 1).reduce((sum, val) => sum + val, 0);
        return val ? relevantRetrieved / (index + 1) : 0;
    });
}

function calculateRecall(relevance) {
    const totalRelevance = relevance.reduce((sum, val) => sum + val, 0);
    return relevance.map((val, index) => {
        const relevantRetrieved = relevance.slice(0, index + 1).reduce((sum, val) => sum + val, 0);
        return totalRelevance > 0 ? relevantRetrieved / totalRelevance : 0;
    });
}

function calculateF1Score(precision, recall) {
    return precision.map((p, index) => {
        const r = recall[index];
        return p + r > 0 ? (2 * p * r) / (p + r) : 0;
    });
}

function calculateMAP(relevance) {
    const precision = calculatePrecision(relevance);
    const totalRelevance = relevance.reduce((sum, val) => sum + val, 0);
    const avgPrecision = relevance.map((val, index) => val ? precision[index] : 0);
    return totalRelevance > 0 ? avgPrecision.reduce((sum, val) => sum + val, 0) / totalRelevance : 0;
}

function calculateNDCG(relevance) {
    const idealRelevance = [...relevance].sort((a, b) => b - a);
    const dcg = relevance.reduce((sum, rel, index) => sum + rel / Math.log2(index + 2), 0);
    const idcg = idealRelevance.reduce((sum, rel, index) => sum + rel / Math.log2(index + 2), 0);
    return idcg > 0 ? dcg / idcg : 0;
}