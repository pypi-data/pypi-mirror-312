import PropTypes from "prop-types";
import React, { useContext } from "react";
import _groupBy from "lodash/groupBy";
import _map from "lodash/map";
import { Label, Icon, Grid } from "semantic-ui-react";
import { withState } from "react-searchkit";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";
import _uniq from "lodash/merge";
import { ClearFiltersButton } from "@js/oarepo_ui";
// TODO: in next iteration, rethink how handling of initialFilters/ignored filters is to be handled
// in the best way

const getLabel = (filter, aggregations) => {
  const aggName = filter[0];
  let value = filter[1];
  const label =
    aggregations[aggName]?.buckets?.find((b) => b.key === value)?.label ||
    value;
  let currentFilter = [aggName, value];
  const hasChild = filter.length === 3;
  if (hasChild) {
    const { label, activeFilter } = getLabel(filter[2]);
    value = `${value}.${label}`;
    currentFilter.push(activeFilter);
  }
  return {
    label: label,
    activeFilter: currentFilter,
  };
};
const ActiveFiltersElementComponent = ({
  filters,
  removeActiveFilter,
  currentResultsState: {
    data: { aggregations },
  },
  ignoredFilters,
}) => {
  const searchAppContext = useContext(SearchConfigurationContext);
  const {
    initialQueryState: { filters: initialFilters },
  } = searchAppContext;
  const allFiltersToIgnore = _uniq([
    ...initialFilters.map((f) => f[0]),
    ...ignoredFilters,
  ]);

  const filtersWithoutInitialFilters = filters?.filter(
    (f) => !allFiltersToIgnore.includes(f[0])
  );
  const groupedData = _groupBy(filtersWithoutInitialFilters, 0);
  return (
    <Grid>
      <Grid.Column only="computer">
        <div className="flex wrap align-items-center">
          {_map(groupedData, (filters, key) => (
            <Label.Group key={key} className="active-filters-group">
              <Label pointing="right">
                <Icon name="filter" />
                {aggregations[key]?.label}
              </Label>
              {filters.map((filter, index) => {
                const { label, activeFilter } = getLabel(filter, aggregations);
                return (
                  <Label
                    className="active-filter-label"
                    key={activeFilter}
                    onClick={() => removeActiveFilter(activeFilter)}
                    type="button"
                    tabIndex="0"
                    aria-label={`Remove filter ${label}`}
                    onKeyPress={(e) => {
                      if (e.key === "Enter" || e.key === " ") {
                        removeActiveFilter(activeFilter);
                      }
                    }}
                  >
                    {label}
                    <Icon name="delete" aria-hidden="true" />
                  </Label>
                );
              })}
            </Label.Group>
          ))}
          <ClearFiltersButton ignoredFilters={ignoredFilters} />
        </div>
      </Grid.Column>
    </Grid>
  );
};

export const ActiveFiltersElement = withState(ActiveFiltersElementComponent);

ActiveFiltersElementComponent.propTypes = {
  filters: PropTypes.array,
  ignoredFilters: PropTypes.array,
  removeActiveFilter: PropTypes.func.isRequired,
  currentResultsState: PropTypes.shape({
    data: PropTypes.shape({
      aggregations: PropTypes.object,
    }).isRequired,
  }).isRequired,
};

ActiveFiltersElementComponent.defaultProps = { ignoredFilters: [] };
