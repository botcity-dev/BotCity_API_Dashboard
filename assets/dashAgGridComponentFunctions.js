var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};

dagcomponentfuncs.TaskErrorTooltip = function (props) {
    info = [
        React.createElement('h5', {}, props.data.bot + ' - ' + props.data.automations),
        React.createElement('p', {}, props.data.error_message),
    ];
    return React.createElement(
        'div',
        {
            style: {
                border: '2pt solid white',
                backgroundColor: props.color || 'grey',
                padding: 10,
                whiteSpace: 'pre-wrap'
            },
        },
        info
    );
};

dagcomponentfuncs.ConnectionErrorTooltip = function (props) {
    info = [
        React.createElement('h5', {}, props.data.name),
        React.createElement('p', {}, props.data.failed_connections),
    ];
    return React.createElement(
        'div',
        {
            style: {
                border: '2pt solid white',
                backgroundColor: props.color || 'grey',
                padding: 10,
                whiteSpace: 'pre-wrap'
            },
        },
        info
    );
};