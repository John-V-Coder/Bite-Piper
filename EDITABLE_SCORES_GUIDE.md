# ✏️ Editable Priority Scores - User Guide

## 🎯 Overview

The **Editable Scores Feature** is the core functionality of BITE-PIPER, allowing users to manually adjust priority scores and see real-time impact on funding allocation. This empowers decision-makers to:

- 🔧 **Override automated calculations** with expert judgment
- 📊 **Explore what-if scenarios** by adjusting scores
- ⚖️ **Balance competing priorities** between regions
- 🎯 **Fine-tune allocations** based on policy goals
- 🔄 **Compare automated vs. manual** approaches

---

## 🚀 Quick Start

### 1. **Calculate Initial Allocation**
- Enter total budget (e.g., $1,000,000)
- Click **"🚀 Calculate Allocation"**
- System shows automated priority scores

### 2. **Edit Priority Scores**
- Adjust scores using:
  - **Number input** (type exact value)
  - **Range slider** (drag to adjust)
  - **Quick action buttons** (preset values)
- Allocation updates automatically (500ms delay)

### 3. **Review Changes**
- See updated allocation in real-time
- Compare custom vs. original scores
- Export results for reporting

---

## 📝 How to Edit Scores

### Method 1: Direct Input
```
Type exact value in score field
Range: 0.000 - 1.000
Example: 0.850 → CRITICAL priority
```

### Method 2: Slider
```
Drag slider left (decrease) or right (increase)
Precision: 0.01 increments
Visual feedback: Immediate
```

### Method 3: Quick Action Buttons
```
🔴 Set CRITICAL (1.0)    → Maximum priority
🟠 Set HIGH (0.6)        → High priority
🟡 Set MEDIUM (0.4)      → Medium priority
```

---

## 🎯 Priority Level Thresholds

| Score Range | Priority Level | Color | Allocation Weight |
|-------------|----------------|-------|-------------------|
| **≥ 0.70** | 🔴 CRITICAL | Red | 40% |
| **0.50 - 0.69** | 🟠 HIGH | Orange | 30% |
| **0.30 - 0.49** | 🟡 MEDIUM | Yellow | 20% |
| **< 0.30** | 🟢 LOW | Green | 10% |

---

## 💡 Use Cases

### 1. **Policy Override**
**Scenario**: Automated system rates RegionA as MEDIUM (0.45), but recent disaster requires urgent funding.

**Action**:
1. Increase RegionA score to 0.90 (CRITICAL)
2. See allocation increase from 32% → 58%
3. Export custom allocation for approval

---

### 2. **Budget Balancing**
**Scenario**: Need to balance funding between 3 regions with limited budget.

**Action**:
1. Start with automated scores (0.85, 0.60, 0.40)
2. Adjust to more balanced (0.70, 0.55, 0.45)
3. Compare allocations: 68%/22%/10% → 52%/31%/17%
4. Choose allocation that meets policy goals

---

### 3. **What-If Analysis**
**Scenario**: Board asks "What if we prioritize education over poverty?"

**Action**:
1. Review automated calculation (poverty-heavy)
2. Create custom scores emphasizing literacy
3. Compare side-by-side
4. Present both scenarios to board

---

### 4. **Expert Judgment**
**Scenario**: Data shows RegionB has low poverty, but field reports indicate hidden need.

**Action**:
1. Automated: RegionB = 0.30 (MEDIUM)
2. Adjust based on field knowledge: 0.55 (HIGH)
3. Document rationale in notes
4. Allocation increases from 15% → 28%

---

## 📊 Real-Time Allocation Impact

### Example: Adjusting One Region

**Initial (Automated)**:
```
RegionA: Score 0.850 (CRITICAL) → $680,000 (68%)
RegionB: Score 0.400 (MEDIUM)   → $320,000 (32%)
```

**After Adjustment** (RegionA: 0.850 → 0.650):
```
RegionA: Score 0.650 (HIGH)     → $565,000 (56.5%)
RegionB: Score 0.400 (MEDIUM)   → $435,000 (43.5%)
```

**Impact**: RegionB gains $115,000 by reducing RegionA priority

---

## 🔄 Comparing Automated vs. Custom

### Visual Indicators

**Automated Allocation**:
- Green checkmark ✅
- "Calculated based on: ..."
- Original scores displayed

**Custom Allocation**:
- Purple badge 🟣
- "Custom score: X.XXX (Original: Y.YYY)"
- Real-time updates

---

## 🎮 Interactive Features

### 1. **Auto-Recalculation**
- Edit any score
- Wait 500ms
- Allocation updates automatically
- No button click needed!

### 2. **Reset to Calculated**
- Click **"🔄 Reset to Calculated"**
- Reverts to automated scores
- Clears all custom adjustments

### 3. **Range Slider Sync**
- Move slider → Updates number input
- Type number → Slider position updates
- Always synchronized

### 4. **Visual Feedback**
- Score changes → Color changes
- Priority updates → Badge updates
- Allocation shifts → Progress bars animate

---

## 📤 Exporting Custom Allocations

### Export Options

**JSON Download**:
```json
{
  "budget": 1000000,
  "allocation": "custom",
  "regions": {
    "RegionA": {
      "score": 0.850,
      "amount": 680000,
      "percentage": 68.0,
      "priority": "CRITICAL",
      "type": "custom"
    }
  },
  "timestamp": "2025-01-26T15:30:00Z"
}
```

**Print Report**:
- Formatted for printing
- Includes all scores
- Shows custom vs. calculated
- Ready for presentation

---

## 🧮 Allocation Formula

### How Custom Scores Affect Allocation

```
For each region:
  1. custom_score (0.0 - 1.0) ← User enters
  2. priority_level ← Determined by thresholds
  3. allocation_weight ← MeTTa rule lookup
  4. weighted_score = custom_score × allocation_weight
  5. allocation_ratio = weighted_score / total_weighted
  6. allocated_amount = total_budget × allocation_ratio
```

### Example Calculation

**Budget**: $1,000,000

**Custom Scores**:
- RegionA: 0.900 (CRITICAL, weight 0.40)
- RegionB: 0.500 (HIGH, weight 0.30)

**Calculation**:
```
RegionA: 0.900 × 0.40 = 0.360
RegionB: 0.500 × 0.30 = 0.150
Total weighted: 0.510

RegionA allocation: ($1M × 0.360) / 0.510 = $705,882 (70.6%)
RegionB allocation: ($1M × 0.150) / 0.510 = $294,118 (29.4%)
```

---

## 🎯 Best Practices

### 1. **Start with Automated**
- Review automated calculation first
- Understand why scores were assigned
- Identify areas for adjustment

### 2. **Document Rationale**
- Note why you adjusted scores
- Keep records of custom allocations
- Include in export for auditing

### 3. **Validate Totals**
- Ensure 100% budget allocation
- Check all regions included
- Verify math adds up

### 4. **Compare Scenarios**
- Calculate automated first
- Create custom allocation
- Compare side-by-side
- Choose best approach

### 5. **Iterate and Refine**
- Try different score combinations
- See impact in real-time
- Find optimal balance

---

## 🔍 Score Adjustment Strategies

### Conservative Adjustment
```
Original: 0.850 → Custom: 0.800
Change: -0.050 (small tweak)
Use when: Minor refinement needed
```

### Moderate Adjustment
```
Original: 0.600 → Custom: 0.450
Change: -0.150 (significant change)
Use when: Policy shift required
```

### Aggressive Adjustment
```
Original: 0.400 → Custom: 0.900
Change: +0.500 (major override)
Use when: Emergency or special circumstances
```

---

## 📊 Monitoring Impact

### Key Metrics to Watch

**Per Region**:
- Score change (before → after)
- Priority level change
- Allocation change ($ and %)
- Percentage of total budget

**Overall**:
- Total allocated (should = 100%)
- Distribution fairness
- Policy alignment
- Stakeholder satisfaction

---

## 🚨 Validation & Safeguards

### Automatic Validation

✅ **Score Range**: Must be 0.0 - 1.0  
✅ **Budget Total**: Always equals 100%  
✅ **Number Format**: Validates decimal input  
✅ **Error Messages**: Clear feedback on issues  

### Manual Checks

- [ ] All regions have valid scores
- [ ] Allocation matches intent
- [ ] Documented rationale exists
- [ ] Export successful

---

## 💻 Technical Details

### HTMX Integration

```html
<form hx-post="/recalculate-custom/"
      hx-target="#allocation-display"
      hx-trigger="change delay:500ms">
```

**How it works**:
1. User changes score
2. HTMX waits 500ms (debounce)
3. POST request to `/recalculate-custom/`
4. Django recalculates allocation
5. Returns HTML partial
6. HTMX injects into `#allocation-display`
7. User sees updated allocation

### Data Flow

```
User Input (score)
    ↓
JavaScript (validation)
    ↓
HTMX (POST request)
    ↓
Django View (recalculate_custom)
    ↓
BITE-PIPER (allocate_funding)
    ↓
MeTTa Engine (apply rules)
    ↓
Template Render
    ↓
HTMX Injection
    ↓
User sees result
```

---

## 🎓 Training Scenarios

### Beginner Exercise
1. Calculate with default budget
2. Increase one region by 0.1
3. Observe allocation change
4. Reset to calculated

### Intermediate Exercise
1. Balance 3 regions equally
2. All scores to 0.500
3. See equal distribution
4. Export results

### Advanced Exercise
1. Create policy-driven allocation
2. Prioritize education (literacy scores)
3. Compare to poverty-driven
4. Present both scenarios
5. Document decision rationale

---

## 📚 Related Documentation

- **System Architecture**: `ARCHITECTURE.md`
- **Allocation Formula**: `FUNDING_ALLOCATION_GUIDE.md`
- **Django Integration**: `DJANGO_HTMX_INTEGRATION.md`
- **Quick Reference**: `FUNDING_ALLOCATION_SUMMARY.md`

---

## 🎉 Benefits of Editable Scores

### For Decision Makers
- ✅ **Control**: Override automated calculations
- ✅ **Flexibility**: Adjust based on changing conditions
- ✅ **Transparency**: See exactly how changes affect allocation
- ✅ **Accountability**: Document custom decisions

### For Analysts
- ✅ **Exploration**: Test different scenarios
- ✅ **Validation**: Verify automated calculations
- ✅ **Refinement**: Fine-tune based on domain knowledge
- ✅ **Reporting**: Export custom allocations

### For Stakeholders
- ✅ **Trust**: Human oversight + automation
- ✅ **Understanding**: Clear cause-and-effect
- ✅ **Participation**: Input into allocation decisions
- ✅ **Auditability**: Track all adjustments

---

## 📞 Support

**Questions?** Check:
- `FUNDING_ALLOCATION_GUIDE.md` - Detailed formulas
- `DJANGO_HTMX_INTEGRATION.md` - Technical setup
- `WHATS_NEW.md` - Feature announcements

---

## ✅ Summary

**Editable Scores Feature**:

🎯 **Main Purpose**: Allow manual override of automated priority scores  
⚡ **Key Benefit**: Real-time allocation recalculation  
🔧 **User Control**: Full flexibility with safeguards  
📊 **Transparency**: Compare automated vs. custom  
📤 **Export**: Save and share custom allocations  
🚀 **Easy to Use**: Intuitive interface with instant feedback  

**Start using it**: http://localhost:8000

---

**Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Last Updated**: 2025
